// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
enum { N = 26 };

// Define a variable to hold size of dictionary
int word_count;
int hash_value;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    hash_value = hash(word);
    // Define a check_node to hash table index which is first node of linked list for word's first letter
    node *check_node = table[hash_value];

    // Iterate over linked list until check_node points NULL meanst end of the list
    while (check_node != NULL)
    {
        // If Node's value and word are match, return true
        if (strcasecmp(check_node -> word, word) == 0)
        {
            return true;
        }

        // Move to next node
        check_node = check_node->next;
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    // If index will be greater than N, Return index % N

    if(toupper(word[0]) - 'A' > N)
    {
        return (toupper(word[0]) - 'A') % N;
    }

    return toupper(word[0]) - 'A';
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    // Read dictionary file
    FILE *dict_f = fopen(dictionary, "r");

    // If file is not opened
    if (dict_f == NULL)
    {
        return false;
    }

/*
    for (int i=0;i<N;i++)
    {
        table[i] = NULL;
    }*/

    // Load hast table for each word in the dictionary file
    char dict_word[LENGTH +1]; // Define char variable to read word from dictionary

    // While it is not the end-of-file
    while (fscanf(dict_f, "%s", dict_word) != EOF)
    {
        // Create a memory space size as much as node
        node *new_node = malloc(sizeof(node));

        // If memory space is not created
        if (new_node == NULL)
        {
            return false;
        }
        hash_value = hash(dict_word);

        // Change the node value with word from dictionary
        strcpy(new_node->word, dict_word);



        if (table[hash_value] == NULL)
        {
            new_node->next = NULL;
            table[hash_value] = new_node;
        }

        else
        {
            new_node->next = table[hash_value];

            // Update the hash table's pointer to new node
            table[hash_value] = new_node;
        }

        // Point the new node's next pointer to beginning of linked list which is hash table pointer


        // Increase word_count to calculate size of dictioanry
        word_count++;
    }

    // Close the file
    fclose(dict_f);

    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    // If dictionary file is opened
    if(word_count > 0)
    {
        return word_count;
    }

    return 0;
}


void free_node(node *n)
{
    if (n->next != NULL)
    {
        free_node(n->next);
    }
    free(n);
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // Define a cursor node to move node by node into linked list


    // Iterate over every linked list in to hash table
    for (int i = 0; i < N; i++)
    {
        if (table[i] != NULL)
        {
            free_node(table[i]);
        }
    }

    // TODO
    return true;
}