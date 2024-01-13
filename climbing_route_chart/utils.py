from .constants import COLOR_MAPPING


def is_dark_color(color):
    """Determines if a given color is dark based on its luminance.

    This function converts a color, which can be a named color or a hex code, to its RGB representation.
    It then calculates the luminance of the color and determines if it is dark. The function uses a simple
    luminance formula to assess the brightness.

    Args:
        color (str): The color to be checked. Can be a hex code or a named color.

    Returns:
        bool: True if the color is dark, False otherwise.
    """
    # Convert color to hex if it's a named color
    color = COLOR_MAPPING.get(color, color)  # Default to color itself if not in mapping
    # Assuming color is a hex code, convert it to RGB
    r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
    # Calculate luminance
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    return luminance < 0.5  # Return True if color is dark


def process_color(color):
    """Processes a color name to convert it to its corresponding hex codes.

    This function handles the conversion of French color names to their respective hex codes.
    It also handles 'MARBREE' colors by parsing and returning a list of individual colors.
    If a color is not found in the mapping, a default gray color is used.

    Args:
        color (str): The color name to be processed, which can be a regular color name or 'MARBREE'.

    Returns:
        list: A list of hex codes corresponding to the processed color(s).
    """

    # Check for 'MARBREE' and handle accordingly
    if "MARBREE" in color:
        # Extract the colors in the brackets
        colors_in_brackets = color.split("(")[-1].split(")")[0]
        # Split the colors and map them to hex codes
        return [COLOR_MAPPING.get(c.strip(), "#808080") for c in colors_in_brackets.split("/")]

    return [COLOR_MAPPING.get(color, "#808080")]  # Return a list with a single color
