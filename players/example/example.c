#include <assert.h>
#include <stdio.h>
#include <stdlib.h>

enum { WHITE, BLACK };

int main(int argc, char **argv)
{
    assert(argc == 3);
    int color; // Not used; only for illustration.
    switch (argv[1][0])
    {
        case 'w': color = WHITE; break;
        case 'b': color = BLACK; break;
        default: assert(0);
    }
    srand(atoll(argv[2]));
    for ( ;; )
    {
        printf("%c%c %c%c\n", rand() % 8 + 'a', rand() % 8 + '1', rand() % 8 + 'a', rand() % 8 + '1');
        // Alternatively, include a promotion piece:
        // printf("%c%c %c%c %c\n", rand() % 8 + 'a', rand() % 8 + '1', rand() % 8 + 'a', rand() % 8 + '1', "qrbn"[rand() % 4]);
        // You don't need to do that if you always want to promote to Queen.
    }
}
