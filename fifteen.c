/**
 * fifteen.c
 *
 * Implements Game of Fifteen (generalized to d x d).
 *
 * Usage: fifteen d
 *
 * whereby the board's d are to be d x d,
 * where d must be in [DIM_MIN,DIM_MAX]
 *
 * Note that usleep is obsolete, but it offers more granularity than
 * sleep and is simpler to use than nanosleep; `man usleep` for more.
 */
 
#define _XOPEN_SOURCE 500

#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

// constants
#define DIM_MIN 3
#define DIM_MAX 9

// board
int board[DIM_MAX][DIM_MAX];

// d
int d;

//blank space coordinates
int bscolumn;
int bsrow;

// prototypes
void clear(void);
void greet(void);
void init(void);
void draw(void);
void swap(int trow, int tcolumn);
bool move(int tile);
bool won(void);

int main(int argc, string argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        printf("Usage: fifteen d\n");
        return 1;
    }

    // ensure valid d
    d = atoi(argv[1]);
    if (d < DIM_MIN || d > DIM_MAX)
    {
        printf("Board must be between %i x %i and %i x %i, inclusive.\n",
            DIM_MIN, DIM_MIN, DIM_MAX, DIM_MAX);
        return 2;
    }

    // open log
    FILE *file = fopen("log.txt", "w");
    if (file == NULL)
    {
        return 3;
    }

    // greet user with instructions
    greet();

    // initialize the board
    init();

    // accept moves until game is won
    while (true)
    {
        // clear the screen
        clear();

        // draw the current state of the board
        draw();

        // log the current state of the board (for testing)
        for (int i = 0; i < d; i++)
        {
            for (int j = 0; j < d; j++)
            {
                fprintf(file, "%i", board[i][j]);
                if (j < d - 1)
                {
                    fprintf(file, "|");
                }
            }
            fprintf(file, "\n");
        }
        fflush(file);

        // check for win
        if (won())
        {
            printf("ftw!\n");
            break;
        }

        // prompt for move
        printf("Tile to move: ");
        int tile = get_int();
        
        //quit if user inputs 0 (for testing)
        if (tile == 0)
        {
            break;
        }

        // log move (for testing)
        fprintf(file, "%i\n", tile);
        fflush(file);

        // move if possible, else report illegality
        if (!move(tile))
        {
            printf("\nIllegal move.\n");
            usleep(500000);
        }

        // sleep thread for animation's sake
        usleep(500000);
    }
    
    // close log
    fclose(file);

    // success
    return 0;
}

/**
 * Clears screen using ANSI escape sequences.
 */
void clear(void)
{
    printf("\033[2J");
    printf("\033[%d;%dH", 0, 0);
}

/**
 * Greets player.
 */
void greet(void)
{
    clear();
    printf("WELCOME TO GAME OF FIFTEEN\n");
    usleep(2000000);
}

/**
 * Initializes the game's board with tiles numbered 1 through d*d - 1
 * (i.e., fills 2D array with values but does not actually print them).  
 */
void init(void)
{
    //set initial black space coordinates
    bscolumn = d - 1;
    bsrow = d - 1;
    
    int nums = d * d - 1;
    for(int row = 0; row < d; row++)
    {
        for(int column = 0; column < d; column++)
        {
            board[row][column] = nums;
            nums--;
        }
    }
    
    //swap 1 and 2 if board has even tiles
    if(d % 2 == 0)
    {
        int temp = board[d - 1][d - 2];
        board[d - 1][d - 2] = board[d - 1][d - 3];
        board[d - 1][d - 3] = temp;
    }
}

/**
 * Prints the board in its current state.
 */
void draw(void)
{
    for(int row = 0; row < d; row++)
    {
        for(int column = 0; column < d; column++)
        {
            if(board[row][column] == 0)
            {
                printf("  _");
            }
            else
            {
                printf("%3i", board[row][column]);
            }
        }
        printf("\n");
    }
}

/**
 * Swaps the blank tile if move is legal
 */
void swap(int trow, int tcolumn)
{
    int temp = board[bsrow][bscolumn];
    board[bsrow][bscolumn] = board[trow][tcolumn];
    board[trow][tcolumn] = temp;
    bsrow = trow;
    bscolumn = tcolumn;
}    

/**
 * If tile borders empty space, moves tile and returns true, else
 * returns false. 
 */
bool move(int tile)
{
    int trow;
    int tcolumn;
    
    //find coordinates of tile to move
    for(int row = 0; row < d; row++)
    {
        for(int column = 0; column < d; column++)
        {
            if(board[row][column] == tile){
                trow = row;
                tcolumn = column;
                break;
                break;
            }        
        }
    }
    
    //check if move is legal
    if((trow - 1 == bsrow && tcolumn == bscolumn) || (trow + 1 == bsrow && tcolumn == bscolumn) || (trow == bsrow && tcolumn - 1 == bscolumn) || (trow == bsrow && tcolumn + 1 == bscolumn))
    {
        swap(trow, tcolumn);
        return true;
    }
    else
    {
        return false;
    }
    
}

/**
 * Returns true if game is won (i.e., board is in winning configuration), 
 * else false.
 */
bool won(void)
{
    int num = 1;
    int wcount = 0;
    for(int row = 0; row < d; row++)
    {
        for(int column = 0; column < d; column++)
        {
            if(board[row][column] == num)
            {
                wcount++;
            }
            num++;
        }
    } 
    if(wcount == d * d - 1)
    {
        return true;
    }
    else
    {
        return false;
    }
}