#ifndef luna_value_h
#define luna_value_h

#include "common.h"

// numbers are stored as double values
typedef double Value;

typedef struct {
    int capacity;
    int count;
    
    Value* values;
} ValueArray;

void initValueArray(ValueArray* array);
void writeValueArray(ValueArray* array, Value value);
void freeValueArray(ValueArray* array);

void printValue(Value value);

#endif
