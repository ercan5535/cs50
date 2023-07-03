#include "helpers.h"
#include <math.h>
#include <stdio.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    int average;

    // iterate over every row
    for (int row = 0; row < height; row++)
    {
        // iterate over every column
        for (int col = 0; col < width; col++)
        {
            // calculate the average between Red, Green, Blue
            average = round((image[row][col].rgbtRed + image[row][col].rgbtGreen + image[row][col].rgbtBlue) / 3.0);

            // update every colour with avarage
            image[row][col].rgbtRed = average;
            image[row][col].rgbtGreen = average;
            image[row][col].rgbtBlue = average;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp;

    // iterate over every row
    for (int row = 0; row < height; row++)
    {
        // iterate over every column
        for (int col = 0; col < width / 2 ; col++)
        {
            // swap the pixels
            temp = image[row][col];
            image[row][col] = image[row][width - (col + 1)];
            image[row][width - (col + 1)] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Create a copy of image to calculate avarage from old pixels
    RGBTRIPLE temp[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            temp[i][j] = image[i][j];
        }
    }

    float sum_red, sum_green, sum_blue;
    int pixel_count;

    // iterate over every row
    for (int row = 0; row < height; row++)
    {
        // iterate over every column
        for (int col = 0; col < width; col++)
        {
            sum_red = sum_green = sum_blue = pixel_count = 0;
            // iterate over the every pixel which surrounds to image[row][col] pixel
            for (int i = row - 1; i <= row + 1; i++)
            {
                for (int j = col - 1; j <= col + 1; j++)
                {
                    // if image[i][j] is not at the out of the image
                    if (!(i < 0) && !(i >= height) && !(j < 0) && !(j >= width))
                    {
                        sum_red += temp[i][j].rgbtRed;
                        sum_green += temp[i][j].rgbtGreen;
                        sum_blue += temp[i][j].rgbtBlue;

                        pixel_count++;
                    }
                }
            }

            // update the current pixel with average of surrounded pixels
            image[row][col].rgbtRed = round(sum_red / pixel_count);
            image[row][col].rgbtGreen = round(sum_green / pixel_count);
            image[row][col].rgbtBlue = round(sum_blue / pixel_count);
        }
    }

    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    // define edge matrixes Gx and Gy
    int Gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int Gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};

    int gx_red, gy_red, gx_green, gy_green, gx_blue, gy_blue, new_red, new_green, new_blue;

    // Create a copy of image
    RGBTRIPLE temp[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            temp[i][j] = image[i][j];
        }
    }

    // iterate over every row
    for (int row = 0; row < height; row++)
    {
        // iterate over every column
        for (int col = 0; col < width; col++)
        {
            gx_red = 0, gy_red = 0, gx_green = 0, gy_green = 0, gx_blue = 0, gy_blue = 0;

            // iterate over the every pixel which surrounds to image[row][col] pixel
            for (int i = row - 1; i <= row + 1; i++)
            {
                for (int j = col - 1; j <= col + 1; j++)
                {
                    // if image[i][j] is not at the out of the image
                    if (!(i < 0) && !(i >= height) && !(j < 0) && !(j >= width))
                    {
                        // multiply surround pixel and its Edge matrix value
                        gx_red += temp[i][j].rgbtRed * Gx[i - row + 1][j - col  + 1];
                        gx_green += temp[i][j].rgbtGreen * Gx[i - row + 1 ][j - col + 1];
                        gx_blue += temp[i][j].rgbtBlue * Gx[i - row + 1][j - col + 1];

                        gy_red += temp[i][j].rgbtRed * Gy[i - row + 1][j - col + 1];
                        gy_green += temp[i][j].rgbtGreen * Gy[i - row + 1][j - col + 1];
                        gy_blue += temp[i][j].rgbtBlue * Gy[i - row + 1][j - col + 1];
                    }
                }
            }
            // Calculate Edge value for each colour component
            new_red = round(sqrt(gx_red * gx_red + gy_red * gy_red));
            new_green = round(sqrt(gx_green * gx_green + gy_green * gy_green));
            new_blue = round(sqrt(gx_blue * gx_blue + gy_blue * gy_blue));

            // update original image with calculated edge matrix value
            image[row][col].rgbtRed = new_red > 255 ? 255 : new_red;
            image[row][col].rgbtGreen = new_green > 255 ? 255 : new_green;
            image[row][col].rgbtBlue = new_blue > 255 ? 255 : new_blue;
        }
    }

    return;
}
