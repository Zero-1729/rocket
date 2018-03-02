#include <stdio.h>

#include "../utils/common.h"
#include "../utils/chunk.h"
#include "../utils/debug.h"
#include "../utils/value.h"


int main() {

	Chunk chunk;

	// initialize chunk
    initChunk(&chunk);

	// write to chunk
    writeChunk(&chunk, OP_RETURN, 99);

    // dissasemble chunk
    dissChunk(&chunk, "test chunk");

	// free chunk
    freeChunk(&chunk);

	return 0;
}
