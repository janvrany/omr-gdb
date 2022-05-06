import gdb

__arch = gdb.selected_inferior().architecture()

U_64    = __arch.integer_type(64, False)
I_64    = __arch.integer_type(64, True)
UDATA   = __arch.integer_type(64, False)
U_32    = __arch.integer_type(32, False)
U_16    = __arch.integer_type(16, False)
U_8     = __arch.integer_type(8,  False)
IDATA   = __arch.integer_type(64, True)
I_32    = __arch.integer_type(32, True)
I_16    = __arch.integer_type(16, True)
I_8     = __arch.integer_type(8,  True)
BOOLEAN = U_32

U_8_ptr = U_8.pointer()
U_32_ptr= U_32.pointer()
UDATA_ptr = UDATA.pointer()
