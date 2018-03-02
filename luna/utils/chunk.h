#ifndef luna_chunk_h
#define luna_chunk_h

#include "common.h"
#include "value.h"

typedef enum {
    OP_RETURN,
    OP_CONSTANT,
    OP_CONSTANT_LONG,
} OPCODE;

typedef struct {
    int count; // number of elms in use
    int capacity; // number of elms in array
    uint8_t* code;

    int* lines; // List to track of line num in source code
    ValueArray constants;
} Chunk;

// C has no constructs so we declare new chunks as fn calss
void initChunk(Chunk* chunk);

void freeChunk(Chunk* chunk);

// To append a chunk we use the following function
// Providing it with the "chunk" and "bytes" to write in it
void writeChunk(Chunk* chunk, uint8_t byte, int line);

void writeConstant(Chunk* chunk, Value, int line);

int addConstant(Chunk* chunk, Value value);

#endif
