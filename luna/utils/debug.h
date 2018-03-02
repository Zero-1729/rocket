#ifndef luna_debug_h
#define luna_debug_h

#include "chunk.h"

void dissChunk(Chunk* chunk, const char* name);
int dissInstruction(Chunk* chunk, int i);

#endif
