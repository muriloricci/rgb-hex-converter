import re
import requests

hex_dec = {
    "A": 10,
    "B": 11,
    "C": 12,
    "D": 13,
    "E": 14,
    "F": 15,
    10: "A",
    11: "B",
    12: "C",
    13: "D",
    14: "E",
    15: "F"
}

class Colour:
    def __init__(self, colour):
        self.colour = colour
        self.name = get_colour_name(colour)
        self.type = get_colour_type(colour)
        self.r, self.g, self.b = get_rgb(colour)
        self.hex = get_hex(colour)

    def __str__(self):
        square = "\u2588\u2588"
        output = f"\nName: {self.name}"
        output += f"\nType: {self.type.upper()}"
        output += f"\nRGB: ({self.r}, {self.g}, {self.b})"
        output += f"\nHEX: #{self.hex}"
        output += f"\nSample: \033[38;2;{self.r};{self.g};{self.b}m{square}\033[0m"

        return output

def main():
    colour = Colour(input("Colour: "))
    print(colour)

# Get colour type (valid options: RGB, HEX)
def get_colour_type(colour):
    hex = re.search(r"^#*([0-9a-fA-F]{6})$", colour.strip())
    rgb = re.search(r"(\d{1,3})\D+(\d{1,3})\D+(\d{1,3})", colour)

    if hex:
        if len(hex.group(1)) == 6:
            return "hex"
        else:
            raise ValueError("Hexadecimal colours must have six digits")
    elif rgb:
        if 0 <= int(rgb.group(1)) < 256 and 0 <= int(rgb.group(2)) < 256 and 0 <= int(rgb.group(3)) < 256:
            return "rgb"
        else:
            raise ValueError("RGB colour values must be between 0 and 255")

# Get colour name from TheColorAPI.com API
def get_colour_name(colour):
    if get_colour_type(colour) == "hex":
        colour = colour.lstrip("#")
        url = f"https://www.thecolorapi.com/id?hex={colour}&format=json"
    elif get_colour_type(colour) == "rgb":
        url = f"https://www.thecolorapi.com/id?hex={get_hex(colour)}&format=json"

    try:
        r = requests.get(url)
        r.raise_for_status()
        name = r.json()['name']['value']
        return name
    except requests.exceptions.HTTPError as e:
        print(f"Error: {e}")
        return "Unknown colour"

# Convert HEX values to RGB (decimals) using dict
def get_rgb(colour):
    if get_colour_type(colour) == "rgb":
        rgb = re.search(r"(\d{1,3})\D+(\d{1,3})\D+(\d{1,3})", colour)
        red = int(rgb.group(1))
        green = int(rgb.group(2))
        blue = int(rgb.group(3))
    elif get_colour_type(colour) == "hex":
        colour = colour.lstrip("#")
        red_hex = colour[:2]
        green_hex = colour[2:][:2]
        blue_hex = colour[-2:]

        red = (int(hex_dec.get(red_hex[0].upper(), red_hex[0])) * 16) + int(hex_dec.get(red_hex[1].upper(), red_hex[1]))
        green = (int(hex_dec.get(green_hex[0].upper(), green_hex[0])) * 16) + int(hex_dec.get(green_hex[1].upper(), green_hex[1]))
        blue = (int(hex_dec.get(blue_hex[0].upper(), blue_hex[0])) * 16) + int(hex_dec.get(blue_hex[1].upper(), blue_hex[1]))

    return red, green, blue

# Get HEX values from a valid RGB or HEX input
def get_hex(colour):
    if get_colour_type(colour) == "rgb":
        rgb = re.search(r"(\d{1,3})\D+(\d{1,3})\D+(\d{1,3})", colour)
        red = int(rgb.group(1))
        green = int(rgb.group(2))
        blue = int(rgb.group(3))

        red_digit1 = red // 16
        red_digit2 = red % 16
        red_digit = get_hex_dec_convert(red_digit1) + get_hex_dec_convert(red_digit2)

        green_digit1 = green // 16
        green_digit2 = green % 16
        green_digit = get_hex_dec_convert(green_digit1) + get_hex_dec_convert(green_digit2)

        blue_digit1 = blue // 16
        blue_digit2 = blue % 16
        blue_digit = get_hex_dec_convert(blue_digit1) + get_hex_dec_convert(blue_digit2)

        return f"{red_digit}{green_digit}{blue_digit}"
    elif get_colour_type(colour) == "hex":
        return colour.upper().lstrip("#")

# Convert RGB to HEX, and HEX to RGB; when their value is bigger than 9
def get_hex_dec_convert(digit):
    digit = hex_dec.get(digit, digit)
    return f"{digit}"

if __name__ == "__main__":
    main()