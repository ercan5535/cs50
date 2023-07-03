#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;

    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 | height > 8); //Take user input

    for (int stair = 0; stair < height; stair++) //Loop stair by stair
    {
        for (int i = 1; i < (height - stair); i++) //Left side gap
        {
            printf(" ");
        }

        for (int i = 0; i <= stair; i++) //Left side bricks
        {
            printf("#");
        }

        printf("  "); //Gap between left and right side bricks

        for (int i = 0; i <= stair; i++) //Right side bricks
        {
            printf("#");
        }

        printf("\n"); //New line for next stair
    }
}