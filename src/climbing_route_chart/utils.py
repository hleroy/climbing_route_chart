import re
import unicodedata

from .constants import COLOR_MAPPING


def interpolate_gradient_middle_color(colors):
    """Calculate the interpolated middle color of a gradient.

    For gradients with multiple colors, this function calculates the RGB values
    at the 50% point of the gradient by interpolating between color stops.

    Args:
        colors (list): List of hex color codes in the gradient.

    Returns:
        str: Hex color code representing the middle color of the gradient.
    """
    if len(colors) == 1:
        return colors[0]

    # Calculate which segment the 50% point falls in
    num_segments = len(colors) - 1
    segment_size = 1.0 / num_segments
    middle_position = 0.5

    segment_index = int(middle_position / segment_size)
    # Ensure we don't go out of bounds
    segment_index = min(segment_index, num_segments - 1)

    # Calculate position within the segment (0.0 to 1.0)
    segment_start = segment_index * segment_size
    position_in_segment = (middle_position - segment_start) / segment_size

    # Get the two colors to interpolate between
    color1 = colors[segment_index]
    color2 = colors[segment_index + 1]

    # Convert hex to RGB
    r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
    r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)

    # Interpolate
    r = int(r1 + (r2 - r1) * position_in_segment)
    g = int(g1 + (g2 - g1) * position_in_segment)
    b = int(b1 + (b2 - b1) * position_in_segment)

    # Convert back to hex
    return f"#{r:02x}{g:02x}{b:02x}"


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
    returning a list of individual colors or hex codes. If a color is not found in the mapping, a default gray color
    is used and a warning is printed.

    Args:
        color (str): The color name or hex code to be processed, which can be a regular color name, hex code,
        or 'MARBREE'/'MARBLES'.

    Returns:
        list: A list of hex codes corresponding to the processed color(s).
    """

    def is_hex_code(s):
        """Check if a string is a valid hex code."""
        if len(s) == 7 and s.startswith("#"):
            try:
                int(s[1:], 16)
                return True
            except ValueError:
                return False
        return False

    # Check if the input is already a hex code
    if is_hex_code(color):
        return [color]

    # Convert color name to upper case for case-insensitive comparison
    color = color.upper()

    # Normalize accented characters (e.g. "MARBRÉE" -> "MARBREE") for comparison
    color_normalized = unicodedata.normalize("NFD", color)
    color_normalized = "".join(c for c in color_normalized if unicodedata.category(c) != "Mn")

    # Check for 'MARBREE' or 'MARBLES' and handle accordingly
    if "MARBREE" in color_normalized or "MARBLES" in color_normalized:
        # Extract the colors in the brackets
        colors_in_brackets = color.split("(")[-1].split(")")[0]
        # Split the colors and map them to hex codes or validate if already hex
        hex_codes = []
        for c in colors_in_brackets.split("/"):
            c = c.strip()
            if is_hex_code(c):
                hex_codes.append(c)
            elif c.upper() in COLOR_MAPPING:
                hex_codes.append(COLOR_MAPPING[c.upper()])
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
