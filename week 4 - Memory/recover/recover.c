#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>


int main(int argc, char *argv[])
{
    typedef uint8_t BYTE; //define a type with 8 bit 1 byte
    BYTE buffer[512]; // define a 512 bayt buffer block to read data
    FILE *output_file = NULL; // define output_file as global here

    char filename[8]; //define output file name
    int jpeg_counter = 0;

    // check command line usage is correct
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    // read file
    FILE *input_file = fopen(argv[1], "r");

    //check file opened without problem
    if (input_file == NULL)
    {
        printf("Could not open file");
        return 1;
    }

    // while fread does not return NULL
    while (fread(buffer, sizeof(BYTE), 512, input_file))
    {
        // check is this a beggining of jpeg
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && ((buffer[3] & 0xf0) == 0xe0))
        {
            // check if first jpeg, if first dont close the current one
            if (jpeg_counter != 0)
            {
                fclose(output_file);
            }

            sprintf(filename, "%03i.jpg", jpeg_counter); // assign file_name as 001.jpg, 002.jpg ...
            output_file = fopen(filename, "w"); // create a file to write with file_name
            jpeg_counter++; // increase jpeg_counter by one

        }

        // check output file created without problem
        if (output_file != NULL)
        {
            // write this 512 byte block on the output_file which is craated as 001.jpg, 002.jpg...
            fwrite(buffer, sizeof(BYTE), 512, output_file);
        }
    }

    fclose(output_file); //close the current output file at the end of operation
    fclose(input_file); //close the input file at the end of operation

}