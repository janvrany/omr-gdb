#
# This makefile is provisional, should be replaced with
# autoconf / cmake.
#

ifndef OMR_BINARY
 ifndef OMR_BUILD_DIR
  $(error OMR_BINARY nor OMR_BUIlD_DIR specified, please run $(MAKE) OMR_BUILD_DIR=... or OMR_BINARY=...)
 else
  OMR_BINARIES=$(OMR_BUILD_DIR)/fvtest/compilertriltest/comptest
 endif
else
  OMR_BINARIES=$(OMR_BINARY)
endif

OMR_SCRIPTS=$(patsubst %,%-gdb.py,$(OMR_BINARIES))

all: $(OMR_SCRIPTS)

$(OMR_SCRIPTS): omr-gdb.py.in
	sed "s#@OMR_GDB_DIR@#$(shell realpath $(shell dirname $<))#g" $< > $@

clean:
	rm $(OMR_SCRIPTS)