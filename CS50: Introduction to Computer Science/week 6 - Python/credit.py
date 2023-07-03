from cs50 import get_string

card_number = get_string("Number :") # get user input

total_sum = 0 # assign total digit sum

# iterate over every digit with its index
for ind, number in enumerate(reversed(card_number)):
    # Add the digits from first digit by twos to total_sum
    if ind % 2 == 0:
        total_sum += int(number)
    # Multiply every other digit by 2, starting with the number’s second-to-last digit, add to total_sum
    else:
        number = int(number) * 2
        # If multiplied number is bigger than 9, get sum of its digits
        if number > 9:
            total_sum += int((number % 100) / 10) + (number % 10)
        else:
            total_sum += number

# if total_sum is the power of 10, it is Valid card number
if total_sum % 10 != 0:
    print("INVALID\n")

# Check Visa, Amex or Mastercard
else:
    if (len(card_number) == 13 or len(card_number) == 16) and card_number[0] == "4":
        print("VISA\n")

    if len(card_number) == 16 and (card_number[0:2] == "51" or card_number[0:2] == "52" or card_number[0:2] == "53" or card_number[0:2] == "54"  or card_number[0:2] == "55"):
        print("MASTERCARD\n")

    if len(card_number) == 15 and (card_number[0:2] == '34' or card_number[0:2] == '37'):
        print("AMEX\n")
