#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(void)
{
    FILE *input = fopen("output", "rb");
    int board[4][4];
    for (int i = 0; i < 4; i++)
    {
        for(int j = 0; j < 4; j++)
        {
            fread(&board[i][j], sizeof(int), 1, input);
        }
    }
}