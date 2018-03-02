TESTS=tests
UTILS=utils
OUT=../dist/C

luna: main.c
	cc $(UTILS)/*.c main.c -o $(OUT)/luna

test_bytecode_alloc: $(TESTS)/test_bytecode_allocs.c
	cc $(UTILS)/memory.c $(UTILS)/chunk.c $(UTILS)/value.c $(TESTS)/test_bytecode_allocs.c -o test_bytecode_allocs

test_diss: $(TESTS)/test_diss.c
	cc $(UTILS)/memory.c $(UTILS)/chunk.c $(UTILS)/debug.c $(UTILS)/value.c  $(TESTS)/test_diss.c -o test_diss

test_constants: $(TESTS)/test_constants.c
	cc $(UTILS)/memory.c $(UTILS)/chunk.c $(UTILS)/debug.c $(UTILS)/value.c $(TESTS)/test_constants.c -o test_constant

clean:
	rm $(OUT)/luna
	rm test_*
