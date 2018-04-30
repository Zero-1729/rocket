#include <stdio.h>

#include "../utils/common.h"
#include "../utils/chunk.h"
#include "../utils/debug.h"


int main() {

	Chunk chunk;

	// initialize chunk
    initChunk(&chunk);

    int constant = addConstant(&chunk, 1.2);

    // OP_CONSTANT
    // [ 00 | 23 ]
    //
    // 00 -> opcode
    // 23 -> constamt index

    writeChunk(&chunk, OP_CONSTANT, 89);
    writeChunk(&chunk, constant, 89);
    writeChunk(&chunk, OP_RETURN, 101);

    // dissasemble chunk
    dissChunk(&chunk, "test chunk");

	// free chunk
    freeChunk(&chunk);

	return 0;
}
