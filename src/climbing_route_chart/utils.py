import re

from .constants import COLOR_MAPPING


def is_dark_color(hex_code):
    """Determines if a given color is dark based on its luminance.

    This function assumes the input is a hex color code. It converts the hex code to its RGB representation,
    calculates the luminance of the color, and determines if it is dark. The function uses a simple
    luminance formula to assess the brightness.

    Args:
        hex_code (str): The hex code of the color to be checked.

    Returns:
        bool: True if the color is dark, False otherwise.

    Raises:
        ValueError: If the input is not a valid hex code.
    """
    # Validate hex code format using regular expression
    if not re.match(r"^#[0-9A-Fa-f]{6}$", hex_code):
        raise ValueError("Invalid hex code format. Expected format is '#RRGGBB'.")

    # Convert hex code to RGB
    r, g, b = int(hex_code[1:3], 16), int(hex_code[3:5], 16), int(hex_code[5:7], 16)

    # Calculate luminance
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    return luminance < 0.5  # Return True if color is dark


def process_color(color):
    """Processes a color name to convert it to its corresponding hex codes.

    This function handles the conversion of color names or hex codes to their respective hex codes,
    regardless of the case of the input. It also handles 'MARBREE' (or 'MARBLES') colors by parsing and
    returning a list of individual colors. If a color is not found in the mapping, a default gray color
    is used and a warning is printed.

    Args:
        color (str): The color name or hex code to be processed, which can be a regular color name, hex code,
        or 'MARBREE'/'MARBLES'.

    Returns:
        list: A list of hex codes corresponding to the processed color(s).
    """

    # Check if the input is already a hex code
    if color.startswith("#") and len(color) == 7:
        return [color]

    # Convert color name to upper case for case-insensitive comparison
    color = color.upper()

    # Check for 'MARBREE' or 'MARBLES' and handle accordingly
    if "MARBREE" in color or "MARBLES" in color:
        # Extract the colors in the brackets
        colors_in_brackets = color.split("(")[-1].split(")")[0]
        # Split the colors and map them to hex codes
        hex_codes = []
        for c in colors_in_brackets.split("/"):
            c = c.strip().upper()
            if c in COLOR_MAPPING:
                hex_codes.append(COLOR_MAPPING[c])
            else:
                print(f"Warning: Color '{c}' not found, defaulting to gray.")
                hex_codes.append("#808080")
        return hex_codes

    # Single color processing
    if color in COLOR_MAPPING:
        return [COLOR_MAPPING[color]]
    else:
        print(f"Warning: Color '{color}' not found, defaulting to gray.")
        return ["#808080"]
