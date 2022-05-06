"""
GDB support for OMR Compiler component
"""

import gdb

from gdb.printing import register_pretty_printer
from vdb.printing import CxxPrettyPrinter, CxxCollectionPrettyPrinter

def strip_ns_prefix(printable):
    s = str(printable)
    i = s.rfind('::')
    if i == -1:
        return s
    else:
        return s[i+2:]

def to_addr(val):
    if val.type.code == gdb.TYPE_CODE_PTR:
        return int(val)
    else:
        return int(val.address)



class __TRObject(CxxPrettyPrinter):
    def __init__(self, val):
        super().__init__(val)
        #if val.type.code != gdb.TYPE_CODE_PTR:
        #    val = val.address
        #assert val != None
        #self._val = val


class TR__Node(__TRObject):
    def register(self):
        """
        Does not work yet...
        """
        reg = self._val['_unionA']['_register']
        if (int(reg) & 1) == 1:
            return None
        else:
            return reg

    def to_string(self):
        opcd = strip_ns_prefix(self._val['_opCode']['_opCode'])
        return "0x%x [%s, bci=[%d, %d, -]" % (to_addr(self._val), opcd, self._val['_byteCodeInfo']['_callerIndex'], self._val['_byteCodeInfo']['_byteCodeIndex'])

class TR__Register(__TRObject):
    def to_string(self):
        #regno = self._val['_association']
        regno = 0
        if int(regno) != 0:
            regno = regno.cast(gdb.lookup_type('TR::RealRegister::RegNum'))
            reg = str(regno)
        else:
            reg = 'virtual'
        return "0x%x [V %s]" % (to_addr(self._val), reg)

class TR__RealRegister(__TRObject):
    def to_string(self):
        return "0x%x [R %s]" % (to_addr(self._val), strip_ns_prefix(self._val['_registerNumber']))
        #return "0x%x [R ???]" % (int(self._val))

class TR__Instruction(__TRObject):
    def to_string(self):
        return "0x%x [%s]" % (to_addr(self._val), strip_ns_prefix(self._val['_opcode']['_mnemonic']))


class TR(CxxCollectionPrettyPrinter):
    def __init__(self):
        super().__init__("TR")
        self.add_printer('Node'           , 'TR::Node'        , TR__Node)
        self.add_printer('Register'       , 'TR::Register'    , TR__Register)
        self.add_printer('RealRegister'   , 'TR::RealRegister', TR__RealRegister)
        self.add_printer('Instruction'    , 'TR::Instruction' , TR__Instruction)

register_pretty_printer(gdb.current_progspace(), TR(), replace=True)

# Install breakpoint on TR::trap() so we can debug
# TR_ASSERT()ion failures...
gdb.Breakpoint('TR::trap', internal=True)
