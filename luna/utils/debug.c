#include <stdio.h>

#include "debug.h"
#include "value.h"


void dissChunk(Chunk* chunk, const char* name) {
    printf("== %s ==\n", name);

    // loop through and prints instructions line by line
    for (int i = 0;i < chunk->count;) {
        i = dissInstruction(chunk, i);
    }
}

static int constantInstruction(const char* name, Chunk* chunk, int offset) {
    uint8_t constant = chunk->code[offset + 1];
    printf("%-16s %4d '", name, constant);
    printValue(chunk->constants.values[constant]);
    printf("'\n");

    return offset + 2;
}

static int simpleInstruction(const char* name, int offset) {
    printf("%s\n", name);
    return offset + 1;
}

int dissInstruction(Chunk* chunk, int offset) {
    printf("%04d ", offset);

    // check if opcode is from same line
    // print opcode alligned beneath each other
    // else just print out 'xxxx x OPCODE'
    if ((offset > 0) && (chunk->lines[offset] == chunk->lines[offset - 1])) {
        printf("\t|> ");
    } else {
        printf("%4d ", chunk->lines[offset]);
    }

    uint8_t instruction = chunk->code[offset];

    switch(instruction) {
        case OP_RETURN:
            return simpleInstruction("OP_RETURN", offset);

        case OP_CONSTANT:
            return constantInstruction("OP_CONSTANT", chunk, offset);

        case OP_CONSTANT_LONG:
            return constantInstruction("OP_CONSTANT_LONG", chunk, offset);

        default:
            printf("Unknown opcode %d\n", instruction);
            return offset + 1;
    }
}
