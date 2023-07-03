#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
}
pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    // TODO
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(candidates[i], name) == 0) //If names are matched
        {
            // Create a array has ranks by index, [1 0 2] 2nd candidate has rank1, 1st candidate has rank2, 3rd candidate has rank3
            ranks[rank] = i;
            return true;
        }
    }
    return false;
}

// Update preferences given one voter's ranks
// Preferences[i][j] means voters prefer candidate i over candidate j
void record_preferences(int ranks[])
{
    // TODO
    for (int i = 0; i < candidate_count; i++) //ranks array's order means preferences
    {
        // [1 0 2] means 2nd candidate prefered over 1st candidate, 1st candidate prefered over 3rd candidate
        for (int j = i + 1; j < candidate_count; j++)
        {
            preferences[ranks[i]][ranks[j]] += 1; // so increment one to preferences[1][0] and preferences[0][2]
        }
    }
    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    // TODO
    for (int i = 0; i < candidate_count - 1; i++) // to check only for pairs i<candidate_count-1 and j=i+1
    {
        for (int j = i + 1; j < candidate_count; j++) // for example if candidate_count = 3, check only for 01, 02, 12
        {
            // in preferences matrix value located at i,j > j,i means more voters prefered i th candidate over j th candidate
            if (preferences[i][j] > preferences[j][i])
            {
                pairs[pair_count].winner = i; // so in i,j pair i th candidate is winner
                pairs[pair_count].loser = j; // so in i,j pair j th candidate is loser
                pair_count += 1; // increment pair_count which means we have a new pair, so there is no tie condition
            }

            if (preferences[j][i] > preferences[i][j]) // same thing with opposite condition
            {
                pairs[pair_count].winner = j;
                pairs[pair_count].loser = i;
                pair_count += 1;
            }
        }
    }
    return;
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    // TODO
    int strength, next_strength, highest;

    for (int i = 0; i < pair_count; i++) //iterate over every pair, selection sort
    {
        highest = i; // starts with current pair has highest strength

        // strength means difference between how many people prefered i th candidate over j th candidate and j th candidate over i th candidate
        // for example if 1st candidate is winner and 2nd candidate is loser, strength of this pair = preferences[0][1] - preferences[1][0]
        strength = preferences[pairs[i].winner][pairs[i].loser] - preferences[pairs[i].loser][pairs[i].winner];

        for (int j = i + 1; j < pair_count; j++) //compare i th pair to other pairs in order
        {
            // get the next pair's strength
            next_strength = preferences[pairs[j].winner][pairs[j].loser] - preferences[pairs[j].loser][pairs[j].winner];

            if (next_strength > strength) // if there are pair which has more strength
            {
                highest = j; // changes the highest one
                strength = next_strength; // changes the current strength with highest strength
            }
        }

        if (highest != i) // if there are pair which has more strength, changes the order
        {
            pair temp_pair = pairs[i]; // hold the current pair in a template
            pairs[i] = pairs[highest]; // put the strenghest pair on the current location
            pairs[highest] = temp_pair; // put the current pair which has lower strength to the strenghest pair's location
        }

    }

    return;
}

bool hasCycle(int winner, int loser)
{
    if (locked[loser][winner] == true) // check is there arrow pointing in opposite way
    {
        return true;
    }

    for (int i = 0; i < candidate_count; i++) // check is there a situation for cycle with every candidate
    {
        // locked matrix [loser][i] is true means there is arrow between loser and i th candidate
        // and
        // recursively check if there is a arrow from i th candidate to winner also check arrow from i th candidate to the other candidates by for loop
        // recursively it goes to locked[i][winner] == true condition on the 196th line
        // that means there is a cycle because we have i th candidate which
        // have arrow coming from loser and have arrow pointing winner or pointing a candidate which is pointing winner.. That is a cycle.
        if (locked[loser][i] && hasCycle(winner, i))
        {
            return true;
        }
    }

    return false;
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    // TODO
    for (int i = 0; i < pair_count; i++)
    {
        if (!hasCycle(pairs[i].winner, pairs[i].loser))
        {
            locked[pairs[i].winner][pairs[i].loser] = true;
        }
    }
    return;
}

// Print the winner of the election
void print_winner(void)
{
    // TODO
    bool true_in_column;
    //check every column, if there is a column with all false means nobody pointing this candidate which is winner
    for (int col = 0; col < candidate_count; col++)
    {
        true_in_column = false;

        for (int row = 0; row < candidate_count; row++)
        {
            if (locked[row][col] == true) // means there is true in that location which is not winner
            {
                true_in_column = true;
            }
        }

        if (true_in_column == false) // if true_in_columns variable remain as false that is winner
        {
            printf("%s\n", candidates[col]);
            break;
        }

    }
    return;
}

