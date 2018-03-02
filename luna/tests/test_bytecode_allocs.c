#include <stdio.h>

#include "../utils/common.h"
#include "../utils/chunk.h"

void print_code(Chunk* chunk) {
	printf("\tcode:");
	for (int i = 0;i < chunk->count;i++) {
		if (&chunk->code) printf("\"%s\"\n", &chunk->code[i]);
		else printf("\t\tempty\n");
	}
}

int main() {

	Chunk chunk;

	// initialize chunk
    printf("Initializing chunk at mem: %p\n", chunk.code);
    initChunk(&chunk);

    printf("Contains:\n\tcount: %i\n\tcapacity: %i\n", chunk.count, chunk.capacity);
	print_code(&chunk);

	// write to chunk
    writeChunk(&chunk, OP_RETURN, 102);
    printf("\n\nWrote to chunk\nContains:\n\tcount: %i\n\tcapacity: %i\n", chunk.count, chunk.capacity);
	print_code(&chunk);

	// free chunk
    freeChunk(&chunk);
    printf("\nFree up chunk\nContains:\n\tcount: %i\n\tcapacity: %i\n", chunk.count, chunk.capacity);
	print_code(&chunk);
	printf("\n");

	return 0;
}
