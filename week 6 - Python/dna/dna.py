import csv
import sys


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")

    # TODO: Read database file into a variable
    person_list = [] # Define a list for holding every person data from database
    database_file = sys.argv[1] # Get database file name from command line input

    # Open file
    with open(database_file) as f:
        reader = csv.DictReader(f)

        # Iterate over every person in database and appen into person_list
        for person in reader:
            person_list.append(person)

    # TODO: Read DNA sequence file into a variable
    sequence_file = sys.argv[2] # Get sequence file from command line input

    # Open file
    with open(sequence_file) as f:
        sequence = f.read() # Get sequence from sequence file


    # TODO: Find longest match of each STR in DNA sequence
    # Define a dictionary for holding STRs from database and its longest match
    STR_dict = {}

    # Iterate over every keys from first person
    for STR in person_list[0]:
        # Get the every keys except name
        if STR != 'name':
            # Assign every STR as key and longest match from sequence as value in STR_dict
            STR_dict[STR] = longest_match(sequence, STR)


    # TODO: Check database for matching profiles
    print(check_matching(STR_dict, person_list))

    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run

def check_matching(STR_dict, person_list):
    # Iterate over every person in person_list
    for person in person_list:
        # Initialize person_founded as True
        person_founded = True

        # Check every STR in STR_dict
        for STR in STR_dict:
            # If any STR repeat count doesnt match break loop and update person_founded as False
            if STR_dict[STR] != int(person[STR]):
                person_founded = False
                break

        # If person_founded remains as True, current person STR counts matched
        if person_founded:
            # Return current person's name
            return person['name']

    # If nothing is returned, return 'No Match'
    return 'No match'

main()
