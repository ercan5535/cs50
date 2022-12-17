from cs50 import get_string

def compute_grade(text):

    count_letters = 0
    count_words = 1
    count_sentences = 0

    for char in text:
        if char.isalpha():
            count_letters += 1

        elif char == " ":
            count_words += 1

        elif char == "!" or char == "." or char == "?":
            count_sentences += 1

    L = count_letters / count_words * 100;
    S = count_sentences / count_words * 100;
    grade = 0.0588 * L - 0.296 * S - 15.8;

    return round(grade)



text = get_string("Text: ")

grade = compute_grade(text)

if grade < 1:
    print("Before Grade 1")

elif grade >= 16:
    print("Grade 16+")

else:
    print("Grade %d" % grade)
