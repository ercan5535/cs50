#include <cs50.h>
#include <stdio.h>

int main(void)
{
    long card_number;
    int c0, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15, sum, length = 0, last2_digits;

    do
    {
        card_number = get_long("Number: ");
    }
    while (card_number < 0); //Take card number

    //Get the digits which are multiplied by 2
    c1 = ((card_number % 100) / 10) * 2;
    c3 = ((card_number % 10000) / 1000) * 2;
    c5 = ((card_number % 1000000) / 100000) * 2;
    c7 = ((card_number % 100000000) / 10000000) * 2;
    c9 = ((card_number % 10000000000) / 1000000000) * 2;
    c11 = ((card_number % 1000000000000) / 100000000000) * 2;
    c13 = ((card_number % 100000000000000) / 10000000000000) * 2;
    c15 = ((card_number % 10000000000000000) / 1000000000000000) * 2;

    //Calculate the digit sum for each digit
    c1 = (c1 % 100) / 10 + c1 % 10;
    c3 = (c3 % 100) / 10 + c3 % 10;
    c5 = (c5 % 100) / 10 + c5 % 10;
    c7 = (c7 % 100) / 10 + c7 % 10;
    c9 = (c9 % 100) / 10 + c9 % 10;
    c11 = (c11 % 100) / 10 + c11 % 10;
    c13 = (c13 % 100) / 10 + c13 % 10;
    c15 = (c15 % 100) / 10 + c15 % 10;

    //Get the digits which are not multiplied by 2
    c0 = card_number % 10;
    c2 = (card_number % 1000) / 100;
    c4 = (card_number % 100000) / 10000;
    c6 = (card_number % 10000000) / 1000000;
    c8 = (card_number % 1000000000) / 100000000;
    c10 = (card_number % 100000000000) / 10000000000;
    c12 = (card_number % 10000000000000) / 1000000000000;
    c14 = (card_number % 1000000000000000) / 100000000000000;

    //Calculate the total sum
    sum = c0 + c1 + c2 + c3 + c4 + c5 + c6 + c7 + c8 + c9 + c10 + c11 + c12 + c13 + c14 + c15;

    printf("%d\n", sum);

    if (sum % 10 != 0) //Check Valid or Invalid?
    {
        printf("INVALID\n");
    }

    else //Check Visa or Amex or MasterCard?
    {
        while (card_number > 0) //Find length and last 2 digits
        {
            card_number = card_number / 10;

            if (card_number<100 & card_number>10)
            {
                last2_digits = card_number;
            }

            length++;
        }


        if ((length == 13 || length == 16) && last2_digits / 10 == 4)
        {
            printf("VISA\n");
        }

        if (length == 16 && (last2_digits == 51 || last2_digits == 52 || last2_digits == 53 || last2_digits == 54  || last2_digits == 55))
        {
            printf("MASTERCARD\n");
        }

        if (length == 15 && (last2_digits == 34 || last2_digits == 37))
        {
            printf("AMEX\n");
        }


    }
}