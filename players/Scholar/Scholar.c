// Scholar, by histocrat
// https://codegolf.stackexchange.com/a/195056/30688
// Revision of 2019-10-29 22:12:44Z

#include <assert.h>
#include <stdio.h>
#include <stdlib.h>

enum { WHITE, BLACK };

int main(int argc, char **argv)
{
    assert(argc == 3);
    int color;
    switch (argv[1][0])
    {
        case 'w': color = WHITE; break;
        case 'b': color = BLACK; break;
        default: assert(0);
    }
    if(color == WHITE) {
        printf("e2 e3\n");
        printf("d1 h5\n");
        printf("f1 c4\n");
        printf("h5 f7\n");
    }
    else {
        printf("e7 e6\n");
        printf("d8 h4\n");
        printf("f8 c5\n");
        printf("h4 f2\n");
    }
    srand(atoll(argv[2]));
    for ( ;; )
    {
        printf("%c%c %c%c\n", rand() % 8 + 'a', rand() % 8 + '1', rand() % 8 + 'a', rand() % 8 + '1');
    }
}
