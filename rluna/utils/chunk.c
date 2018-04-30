#include <stdlib.h>

#include "chunk.h"
#include "memory.h"
#include "value.h"

void initChunk(Chunk* chunk) {
    chunk->count = 0;
    chunk->capacity = 0;
    chunk->code = NULL;

    chunk->lines = NULL;
    initValueArray(&chunk->constants);
}

void writeChunk(Chunk* chunk, uint8_t byte, int line) {
    if (chunk->count + 1 > chunk->capacity) {
        int oldCapacity = chunk->capacity;
        chunk->lines = GROW_ARRAY(chunk->lines, int, oldCapacity, chunk->capacity);

        chunk->capacity = GROW_CAPACITY(oldCapacity); // Double capacity

        chunk->code = GROW_ARRAY(chunk->code, uint8_t, oldCapacity, chunk->capacity);
    }

    // if capacity is still larger than count.
    // AKA there is available space
    // We just write the byte of the chunk and INC the count
    chunk->code[chunk->count] = byte;
    chunk->lines[chunk->count] = line;
    chunk->count++;
}

void writeConstant(Chunk* chunk, Value value, int line) {
    // get current value of
    int offset = chunk->constants.count;

    chunk->constants.values[offset] = value;
}

int addConstant(Chunk* chunk, Value value) {
    writeValueArray(&chunk->constants, value);
    return chunk->constants.count - 1;
}

void freeChunk(Chunk* chunk) {
    FREE_ARRAY(uint8_t, chunk->code, chunk->capacity);
    FREE_ARRAY(int, chunk->lines, chunk->capacity);

    freeValueArray(&chunk->constants);
    initChunk(chunk);
}
