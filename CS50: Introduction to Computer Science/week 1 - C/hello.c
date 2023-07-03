#include <stdio.h>
#include <cs50.h>

int main(void)
{
    string name = get_string("What's your name?\n"); //get the name from user and assign as a string

    printf("\nHello, %s!\n", name); //Say hello!

}