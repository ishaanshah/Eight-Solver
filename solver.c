#include <cs50.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

typedef struct
{
    int row;
    int column;
} COORDINATES;

// pointer to board
int **board = NULL;

// dimensions of board
int d;

// track the last move made
int lastMove;

// coordinates for blank space
COORDINATES bsCoordinate;

int nearestNeighbour(int toMove, int possibleMove[4]);
COORDINATES search(int tile);

int main(void)
{
    FILE *input = fopen("output", "rb");
    if(input == NULL)
    {
        return 4;
    }
    
    // read the dimensions of board from file
    fread(&d, sizeof(int), 1, input);
    
    // initialize the board with dimensions of d*d
    board = (int **)malloc(d * sizeof(int));
    for(int i = 0; i < d; i++)
    {
        board[i] = (int *)malloc(d * sizeof(int));
    }
    
    // read the state of board from output file
    for (int i = 0; i < 4; i++)
    {
        for(int j = 0; j < 4; j++)
        {
            fread(&board[i][j], sizeof(int), 1, input);
            printf("%i\n",board[i][j]);
        }
    }
    
    // store coordinates of black space
    bsCoordinate = search(0);
    
    int temp[4] = {13,10,9,8};
    nearestNeighbour(10, temp);
}

int nearestNeighbour(int toMove, int possibleMove[4])
{
    // store coordinates of tile to move
    COORDINATES tCoordinate = search(toMove);
    
    // variable to store coordintaes of possible moves
    COORDINATES pCoordinate;
    
    // array to store distances
    float distance[4];
    
    // calculate the distances of possible moves from tile to move
    for(int i = 0; i < 4; i++)
    {
        pCoordinate = search(possibleMove[i]);
        distance[i] = sqrt(pow((tCoordinate.row - pCoordinate.row), 2) + pow((tCoordinate.column - pCoordinate.column), 2));
        printf("%f\n", distance[i]);
    }
    
    // find the nearest tile
    float smallest = distance[0];
    for(int i = 0; i < 4; i++)
    {
        if(distance[i] < smallest)
        {
            smallest = distance[i]; 
        }
    }
    
    // return possible move
    int temp;
    for(int i = 0; i < 4; i++){
        if(smallest == distance[i])
        {
            temp = i;
        }
    }
    
    return possibleMove[temp]; 
}

COORDINATES search(int tile)
{
    // create new struct to store coordinates of the tile to find
    COORDINATES coordinate;
    
    //find coordinates of tile to move
    for(int row = 0; row < d; row++)
    {
        for(int column = 0; column < d; column++)
        {
            if(board[row][column] == tile){
                coordinate.row = row;
                coordinate.column = column;
                break;
            }        
        }
    }
    return coordinate;
}