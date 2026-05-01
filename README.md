# RGB-HEX CONVERTER
#### Video Demo
https://www.youtube.com/watch?v=uSVWTu3D3DY
#### Description
This is a script created as the final project for the CS50P Harvard University course. A script that assists the user to convert a colour value, either in RGB or HEX format, to the other option between the two.

The main function asks the user for an input of a colour. The colour must be provided with RGB or Hex format.
- RGB format should contain three numbers of three digits maximum each, from 0 to 255.
- Hex format should contain numbers or letters from A to F, for a total of 6 digits.
Assuming users might make some mistakes when providing the input, I included regex search to both validate the input type as well as try to accept some not completely valid inputs but that could still be classified correct.

Once the input is provided, the get_colour_type() function validates whether the provided input is RGB or HEX.

With this information, we then use the get_colour_name() function to make an API request to TheColorAPI endpoint, and get the name of the colour. In case we had a request error, the script tells the user the colour is unknown.

Next, we use the get_rgb() and get_hex() functions to get values in RGB and Hex to be used in the printing:
- get_rgb() returns the R, G and B values in a tuple format
- get_hex() returns the hex value with all letters capitalised, and without a hashtag (this is a personal preference)

Lastly, the get_hex_dec_convert() function assists with converting numbers to letters, and letters to numbers with a dictionary (hex_dec, at the beginning of the code)

Python can natively handle some convertions used in the script, for example converting a base 10 number into a hexadecimal, but I preferred doing these convertions as part of learning process and development of this project.

After all convertions and data collection, the main function creates a colour object, and outputs the data the user, including a square with the input colour used as sample for visualisation.
