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

def main():
    colour = input("Colour: ")

    colour_name = get_colour_name(colour)
    colour_type = get_colour_type(colour)
    r, g, b = get_rgb(colour)
    hex_val = get_hex(colour)
    square = "\u2588\u2588"

    print(f"\nName: {colour_name}")
    print(f"Type: {colour_type.upper()}")
    print(f"RGB: ({r}, {g}, {b})")
    print(f"HEX: #{hex_val}")
    print(f"Sample: \033[38;2;{r};{g};{b}m{square}\033[0m")

# Get colour type (valid options: RGB, HEX)
def get_colour_type(colour):
    rgb = re.search(r"(\d{1,3})\D+(\d{1,3})\D+(\d{1,3})", colour)
    hex = re.search(r"#*([\dabcdefABCDEF]+)", colour)

    if rgb:
        if 0 <= int(rgb.group(1)) < 256 and 0 <= int(rgb.group(2)) < 256 and 0 <= int(rgb.group(3)) < 256:
            return "rgb"
        else:
            raise ValueError("RGB colour values must be between 0 and 255")
    elif hex:
        if len(hex.group(1)) == 6:
            return "hex"
        else:
            raise ValueError("Hexadecimal colours must have six digits")

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

        red = (hex_dec.get(red_hex[0].upper()) * 16) + hex_dec.get(red_hex[1].upper())
        green = (hex_dec.get(green_hex[0].upper()) * 16) + hex_dec.get(green_hex[1].upper())
        blue = (hex_dec.get(blue_hex[0].upper()) * 16) + hex_dec.get(blue_hex[1].upper())

    return red, green, blue

# Get HEX values from a valid RGB or HEX input
def get_hex(colour):
    if get_colour_type(colour) == "rgb":
        rgb = re.search(r"(\d{1,3})\D+(\d{1,3})\D+(\d{1,3})", colour)
        red = int(rgb.group(1))
        green = int(rgb.group(2))
        blue = int(rgb.group(3))

        red_digit1 = red // 16
        red_digit2 = red - (int(red // 16) * 16)
        red_digit = get_hex_dec_convert(red_digit1) + get_hex_dec_convert(red_digit2)

        green_digit1 = green // 16
        green_digit2 = green - (int(green // 16) * 16)
        green_digit = get_hex_dec_convert(green_digit1) + get_hex_dec_convert(green_digit2)

        blue_digit1 = blue // 16
        blue_digit2 = blue - (int(blue // 16) * 16)
        blue_digit = get_hex_dec_convert(blue_digit1) + get_hex_dec_convert(blue_digit2)

        return f"{red_digit}{green_digit}{blue_digit}"
    elif get_colour_type(colour) == "hex":
        return colour.upper()

# Convert RGB to HEX, and HEX to RGB; when their value is bigger than 9
def get_hex_dec_convert(digit):
    digit = hex_dec.get(digit, digit)
    return f"{digit}"

if __name__ == "__main__":
    main()