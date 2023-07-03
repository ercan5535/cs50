#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Points assigned to each letter of the alphabet
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};
char LETTERS[] = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y'};

int compute_score(string word);

int main(void)
{
    // Get input words from both players
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // Score both words
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    if (score1 > score2)
    {
        printf("Player 1 wins!");
    }

    else if (score1 < score2)
    {
        printf("Player 2 wins!");
    }

    else
    {
        printf("Tie!");
    }

}

int compute_score(string word)
{
    int score = 0;
    int char_index;

    for (int i = 0; i < strlen(word); i++)
    {
        char_index = word[i]; //get ASCII index for letter

        if ((char_index >= 65 && char_index <= 90) ||
            (char_index >= 97 && char_index <= 122)) //check only for letters with ASCII number base
        {
            if (isupper(word[i]))
            {
                char_index = char_index - 65; //a-z -> 65-90 in ASCII but we need 0-25
            }

            else
            {
                char_index = char_index - 97; //A-Z -> 97-122 in ASCII but we need 0-25
            }

            score += POINTS[char_index]; //add points to score from POINTS by letter's index
        }

    }

    return score;
}