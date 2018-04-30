#include <stdio.h>

#include "utils/common.h"
#include "utils/chunk.h"
#include "utils/debug.h"


void usage() {

    printf("luna is a tool for managing Rocket source code.\n\n");
    printf("Usage:\n\tluna command [arguments] [file]\n\n");
    printf("The commands are:\n");
    printf("\tbuild\t\tcompile packages and dependencies\n");
    printf("\tinstall\t\tcompile and install packages and dependencies\n");
    printf("\ttest\t\ttest packages\n");
    printf("\tversion\t\tprint Luna version\n\n");
}

void prompt() {
    printf("[Prompt]\tN/A\n");
}

void run() {
    printf("[Running scripts]\tN/A\n");
}

int main(int argc, const char* argv[]) {
    if (argc == 2) {
        run();
    } else if (argc == 1) {
        prompt();
    } else {
        usage();
    }

    return 0;
}
