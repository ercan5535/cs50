#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>


int compute_grade(string text);

int main(void)
{
    // Get input text
    string text = get_string("Text: ");

    // Compute grade for text
    int grade = compute_grade(text);


    if (grade < 1)
    {
        printf("Before Grade 1\n");
    }

    else if (grade >= 16)
    {
        printf("Grade 16+\n");
    }

    else
    {
        printf("Grade %d\n", grade);
    }

}

int compute_grade(string text)
{
    int count_letters = 0;
    int count_words = 1;
    int count_sentences = 0;
    int char_index;

    for (int i = 0; i < strlen(text); i++)
    {
        char_index = text[i]; //get ASCII index

        if ((char_index >= 65 && char_index <= 90) ||
            (char_index >= 97 && char_index <= 122)) //check only for letters with ASCII number base
        {
            count_letters += 1;
        }

        else if (char_index == 32) //check for space
        {
            count_words += 1;
        }

        else if (char_index == 46 || char_index == 33 || char_index == 63) //check for period, exclamation point or question mark
        {
            count_sentences += 1;
        }
    }

    float L = (float) count_letters / (float) count_words * 100;
    float S = (float) count_sentences / (float) count_words * 100;
    float grade = 0.0588 * L - 0.296 * S - 15.8;

    return (int) round(grade);
}