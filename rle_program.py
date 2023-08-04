import console_gfx as gfx
from itertools import groupby
import math

# Converts data (RLE) to a hexadecimal string (without delimiters).
# Ex(RLE): to_hex_string([3, 15, 6, 4]) yields string "3f64".
def to_hex_string(data):
        val = ''
        hex_str = ''
        for i in range(0, len(data)):
                if 0 <= int(data[i]) < 10:
                        val = str(data[i])
                elif int(data[i]) == 10:
                        val = 'a'
                elif int(data[i]) == 11:
                        val = 'b'
                elif int(data[i]) == 12:
                        val = 'c'
                elif int(data[i]) == 13:
                            val = 'd'
                elif int(data[i]) == 14:
                        val = 'e'
                elif int(data[i]) == 15:
                        val = 'f'
                hex_str = hex_str + val
        return hex_str

# Returns number of runs of data in an image data set.
# Ex: count_runs([15, 15, 15, 4, 4, 4, 4, 4, 4]) yields integer 2.
def count_runs(flat_data):
        runs = 0
        counts = [sum(1.0 for _ in group) for _, group in groupby(flat_data)]
        for i in range (0, len(counts)):
                val = math.ceil(counts[i] / 15.0)
                runs += int(val)
        return runs

# Returns encoding (in RLE) of the raw data passed in.
# Ex: encode_rle([15, 15, 15, 4, 4, 4, 4, 4, 4]) yields list [3, 15, 6, 4].
def encode_rle(flat_data):
        counts = [sum(1 for _ in group) for _, group in groupby(flat_data)]
        values = [i[0] for i in groupby(flat_data)]

        rle = []
        for i in range(0, len(counts)):
                if int(counts[i]) <= 15:
                        rle.append(counts[i])
                        rle.append(values[i])
                elif int(counts[i]) > 15:
                        if (int(counts[i]) % 15) == 0:
                                full_runs = int(counts[i]) // 15
                                for j in range(0, full_runs):
                                        rle.append(15)
                                        rle.append(values[i])
                        elif (int(counts[i]) % 15) > 0:
                                full_runs = int(counts[i]) // 15
                                final_run = int(counts[i]) % 15
                                for j in range(0, full_runs):
                                        rle.append(15)
                                        rle.append(values[i])
                                rle.append(final_run)
                                rle.append(values[i])
        return rle


# Returns decompressed size RLE data.
# Ex: get_decoded_length([3, 15, 6, 4]) yields integer 9.
def get_decoded_length(rle_data):
        length = 0
        for i in range(0, len(rle_data), 2):
                length += rle_data[i]
        return length

# Returns the decoded data set from RLE encoded data.
# Ex: decode_rle([3, 15, 6, 4]) yields list [15, 15, 15, 4, 4, 4, 4, 4, 4].
def decode_rle(rle_data):
        flat_data = []
        for i in range(0, len(rle_data), 2):
                for j in range(0, rle_data[i]):
                        flat_data.append(rle_data[i + 1])
        return flat_data

# Translates a string in hexadecimal format (without delimiters) into RLE byte data.
# Ex: string_to_data ("3f64") yields list [3, 15, 6, 4].
def string_to_data(data_string):
        data = list(data_string)
        for i in range(0, len(data)):
                el = data[i].lower()
                if el == 'a':
                        data[i] = 10
                elif el == 'b':
                        data[i] = 11
                elif el == 'c':
                        data[i] = 12
                elif el == 'd':
                        data[i] = 13
                elif el == 'e':
                        data[i] = 14
                elif el == 'f':
                        data[i] = 15
                else:
                        data[i] = int(data[i])
        return data

# Translates  RLE  data  into  a  human-readable  representation.
# Ex: to_rle_string([15, 15, 6, 4]) yields string "15f:64".
def to_rle_string(rle_data):
        rle_str = ''
        for i in range(1, len(rle_data), 2):
                if i < (len(rle_data) - 1):
                        if 0 <= int(rle_data[i]) < 10:
                                rle_data[i] = str(rle_data[i])+':'
                        elif int(rle_data[i]) == 10:
                                rle_data[i] = 'a:'
                        elif int(rle_data[i]) == 11:
                                rle_data[i] = 'b:'
                        elif int(rle_data[i]) == 12:
                                rle_data[i] = 'c:'
                        elif int(rle_data[i]) == 13:
                                rle_data[i] = 'd:'
                        elif int(rle_data[i]) == 14:
                                rle_data[i] = 'e:'
                        elif int(rle_data[i]) == 15:
                                rle_data[i] = 'f:'
                elif i == (len(rle_data) - 1):
                        if 0 <= int(rle_data[i]) < 10:
                                rle_data[i] = str(rle_data[i])
                        elif int(rle_data[i]) == 10:
                                rle_data[i] = 'a'
                        elif int(rle_data[i]) == 11:
                                rle_data[i] = 'b'
                        elif int(rle_data[i]) == 12:
                                rle_data[i] = 'c'
                        elif int(rle_data[i]) == 13:
                                rle_data[i] = 'd'
                        elif int(rle_data[i]) == 14:
                                rle_data[i] = 'e'
                        elif int(rle_data[i]) == 15:
                                rle_data[i] = 'f'
        for j in range (0, len(rle_data)):
                rle_str += str(rle_data[j])
        return rle_str

# Translates a string in human-readable RLE format (with delimiters) into RLE byte data.
# Ex: string_to_rle("15f:64") yields list [15, 15, 6, 4].
def string_to_rle(rle_string):
        rle = rle_string.split(':')
        for i in range(0, len(rle)):
                if len(rle[i]) > 2:
                        el = rle[i]
                        rle[i] = [el[:2], el[2:len(el)]]
                elif len(rle[i]) == 2:
                        el = rle[i]
                        rle[i] = [el[0], el[-1]]
        rle = [num for sublist in rle for num in sublist]
        for j in range(1, len(rle), 2):
                rle[j] = string_to_data(rle[j])
                el = str(rle[j])
                rle[j] = el[1:-1]
        for k in range(0, len(rle)):
                rle[k] = int(rle[k])
        return rle


# The main function begins here. The welcome message, spectrum image, and menu are displayed.
if __name__ == '__main__':
        play: bool = True
        file = "(no data)"
        print("Welcome to the RLE image encoder!\n\n"
              "Displaying Spectrum Image:")
        gfx.ConsoleGfx.display_image(gfx.ConsoleGfx.test_rainbow)
        print('\n', end='')
        while play:
                menu = ("\nRLE Menu\n"
                        "--------\n"
                        "0. Exit\n"
                        "1. Load File\n"
                        "2. Load Test Image\n"
                        "3. Read RLE String\n"
                        "4. Read RLE Hex String\n"
                        "5. Read Data Hex String\n"
                        "6. Display Image\n"
                        "7. Display RLE String\n"
                        "8. Display Hex RLE Data\n"
                        "9. Display Hex Flat Data\n")
                print(menu)
                user_input = input("Select a Menu Option: ")

                # Check if the user input an integer. If not, print error message.
                if user_input.isnumeric() == False:
                        print(user_input.isnumeric())
                        print("Error! Invalid input.")

                # Selecting option 0 will end the program
                elif int(user_input) == 0:
                        play = False

                # Selecting option 1 will allow the user to enter the name of a file load and load the file.
                elif int(user_input) == 1:
                        file_name = input("Enter name of file to load: ")
                        file = gfx.ConsoleGfx.load_file(file_name)

                # Selecting option 2 will load the test image and print a message stating that the test image data is loaded.
                elif int(user_input) == 2:
                        file = gfx.ConsoleGfx.test_image
                        print("Test image data loaded.")

                # Selecting option 3 will allow the user to enter an RLE string and decode it.
                elif int(user_input) == 3:
                        user_str = input("Enter an RLE string to be decoded: ")
                        file = decode_rle(string_to_rle(user_str))

                # Selecting option 4 will allow the user to enter a hex string holding RLE data and decode it.
                elif int(user_input) == 4:
                        user_str = input("Enter the hex string holding RLE data: ")
                        file = decode_rle(string_to_data(user_str))

                # Selecting option 5 will allow the user to enter a hex string holding flat data and decode it.
                elif int(user_input) == 5:
                        user_str = input("Enter the hex string holding flat data: ")
                        file = string_to_data(user_str)

                # Selecting option 6 will print the message "Displaying image..." and display the image representation of the loaded file, or print (no data) if no file has been loaded.
                elif int(user_input) == 6:
                        print("Displaying image...")
                        if file == "(no data)":
                                print(file)
                        else:
                                gfx.ConsoleGfx.display_image(file)

                # Selecting option 7 will print the human-readable RLE representation of the loaded file (with delimiters), or print (no data) if no file has been loaded.
                elif int(user_input) == 7:
                        if file == "(no data)":
                                print(file)
                        else:
                                rle_str = to_rle_string(encode_rle(file))
                                print("RLE representation: " + rle_str)

                # Selecting option 8 will print the RLE hex values of the loaded file (without delimiters), or print (no data) if no file has been loaded.
                elif int(user_input) == 8:
                        if file == "(no data)":
                                print(file)
                        else:
                                rle_hex_str = to_hex_string(encode_rle(file))
                                print("RLE hex values: " + rle_hex_str)

                # Selecting option 9 will print the flat hex values of the loaded file, or print (no data) if no file has been loaded.
                elif int(user_input) == 9:
                        if file == "(no data)":
                                print(file)
                        else:
                                flat_hex_str = to_hex_string(file)
                                print("Flat hex values: " + flat_hex_str)

                # If the user inputs any integer outside of the range 0 - 9 (inclusive), the error message will be printed.
                else:
                        print("Error! Invalid input.")