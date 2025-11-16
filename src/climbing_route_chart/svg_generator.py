import math

import drawsvg as draw

from . import constants
from .utils import is_dark_color


def determine_colors(route, x1, y1, x2, y2):
    """Determines the fill and text colors for a pie chart slice based on the route's color.

    For routes with multiple colors (indicating a gradient), it creates a linear gradient fill.
    For routes with a single color, it uses that color as the fill. It also determines the
    appropriate text color (either black or white) for readability based on the fill color's luminance.

    Args:
        route (pd.Series): The data series representing a single climbing route.
        x1 (float): The x-coordinate of the start point for the gradient.
        y1 (float): The y-coordinate of the start point for the gradient.
        x2 (float): The x-coordinate of the end point for the gradient.
        y2 (float): The y-coordinate of the end point for the gradient.

    Returns:
        tuple: A tuple containing the text color and the path fill (either a single color or a gradient).
    """
    # Determine fill color
    if len(route["Couleur"]) > 1:
        # Create gradient
        gradient = draw.LinearGradient(x1, y1, x2, y2)
        for i, color in enumerate(route["Couleur"]):
            offset = i / (len(route["Couleur"]) - 1)
            gradient.add_stop(offset, color)
        path_fill = gradient
    else:
        # Single color
        path_fill = route["Couleur"][0]

    # Determine text color
    if len(route["Couleur"]) > 1:
        # Gradient case
        text_color = "white"  # Default to white for gradients
    else:
        # Single color
        path_fill = route["Couleur"][0]
        text_color = "white" if is_dark_color(path_fill) else "black"

    return text_color, path_fill


def add_pie_chart_to_svg(drawing, group, center_x, center_y, radius, grade_fs, setter_fs, relay):
    """Adds a pie chart to an SVG drawing based on climbing route data.

    This function creates a pie chart for a given group of climbing routes, adding it to an existing SVG drawing.
    It handles both single-color and gradient fills for the pie slices and adjusts the text color for readability
    based on the background color. The pie chart visualizes the distribution of climbing routes.

    Args:
        drawing (draw.Drawing): The SVG drawing object to which the pie chart will be added.
        group (list of dict): The group of climbing routes data, where each route is represented as a dictionary.
        center_x (float): The x-coordinate of the center of the pie chart.
        center_y (float): The y-coordinate of the center of the pie chart.
        radius (float): The radius of the pie chart.
        grade_fs (int): Font size for the grade labels in the pie chart.
        setter_fs (int): Font size for the route setter names in the pie chart.
        relay (str): The relay number to display on the chart.

    Raises:
        Exception: If an error occurs in drawing the pie chart components.

    Returns:
        None: The function adds components to the SVG drawing but does not return anything.
    """
    num_routes = len(group)
    if num_routes == 0:
        return  # No routes to display

    if num_routes == 1:
        route = group[0]
        x1, y1 = center_x - radius, center_y
        x2, y2 = center_x + radius, center_y
        text_color, path_fill = determine_colors(route, x1, y1, x2, y2)
        text_y = center_y - radius / 2
        drawing.append(draw.Circle(center_x, center_y, radius, fill=path_fill, stroke_width=1, stroke="black"))
        drawing.append(
            draw.Text(text=route["Cotation"], font_size=grade_fs, x=center_x, y=text_y, center=0.5, fill=text_color, font_family="DejaVu Sans")
        )
        drawing.append(
            draw.Text(
                text=route["Ouvreur"], font_size=setter_fs, x=center_x, y=text_y + 12, center=0.5, fill=text_color, font_family="DejaVu Sans"
            )
        )
        # Add Commentaire if present
        if "Commentaire" in route and route["Commentaire"]:
            comment_fs = min(setter_fs, 8)  # Max font size is setter_fs
            drawing.append(
                draw.Text(
                    text=route["Commentaire"],
                    font_size=comment_fs,
                    x=center_x,
                    y=text_y + 12 + setter_fs,
                    center=0.5,
                    fill=text_color,
                    font_family="DejaVu Sans",
                    font_style="italic",
                )
            )

        # Add relay number in a rectangle at the top of the disk
        relay_text = str(relay)
        relay_fs = 17
        rect_width = 14 + (len(relay_text) - 1) * 10  # Dynamic width based on text length
        rect_height = 15
        rect_x = center_x - rect_width / 2
        rect_y = center_y - radius + 5

        drawing.append(draw.Rectangle(rect_x, rect_y, rect_width, rect_height, fill="white", stroke_width=1, stroke="black"))
        drawing.append(
            draw.Text(text=relay_text, font_size=relay_fs, x=center_x, y=rect_y + rect_height / 2 + 1, center=0.5, fill="black", font_family="DejaVu Sans")
        )
        return

    start_angle = 0
    for route in group:
        sweep_angle = 360 / num_routes
        end_angle = start_angle + sweep_angle
        x1, y1 = center_x + radius * math.cos(math.radians(start_angle)), center_y + radius * math.sin(
            math.radians(start_angle)
        )
        x2, y2 = center_x + radius * math.cos(math.radians(end_angle)), center_y + radius * math.sin(
            math.radians(end_angle)
        )

        text_color, path_fill = determine_colors(route, x1, y1, x2, y2)

        path = draw.Path(stroke_width=1, stroke="black", fill=path_fill)
        path.M(center_x, center_y)  # Move to center
        path.l(x1 - center_x, y1 - center_y)  # Line to first point on circumference
        path.A(radius, radius, 0, 0, 1, x2, y2)  # Arc to second point
        path.Z()  # Close path
        drawing.append(path)

        mid_angle = (start_angle + end_angle) / 2
        text_radius_multiplier = 0.6
        text_x = center_x + radius * text_radius_multiplier * math.cos(math.radians(mid_angle))
        text_y = center_y + radius * text_radius_multiplier * math.sin(math.radians(mid_angle)) - 5

        # Adjust text position if it would overlap with relay box at the top (around 270°)
        # The relay box is positioned at the top of the circle, so slices with mid_angle
        # between 240° and 300° need their text moved downward to avoid overlap
        if 240 <= mid_angle <= 300:
            text_y += 15  # Move text downward to clear the relay box
        drawing.append(
            draw.Text(text=route["Cotation"], font_size=grade_fs, x=text_x, y=text_y, center=0.5, fill=text_color, font_family="DejaVu Sans")
        )
        drawing.append(
            draw.Text(text=route["Ouvreur"], font_size=setter_fs, x=text_x, y=text_y + 12, center=0.5, fill=text_color, font_family="DejaVu Sans")
        )
        # Add Commentaire if present
        if "Commentaire" in route and route["Commentaire"]:
            # Calculate font size based on slice angle to fit text
            slice_arc_length = (sweep_angle / 360) * 2 * math.pi * radius * text_radius_multiplier
            comment_fs = min(setter_fs, int(slice_arc_length / len(route["Commentaire"]) *1.5))
            drawing.append(
                draw.Text(
                    text=route["Commentaire"],
                    font_size=comment_fs,
                    x=text_x,
                    y=text_y + 12 + setter_fs,
                    center=0.5,
                    fill=text_color,
                    font_family="DejaVu Sans",
                    font_style="italic",
                )
            )

        start_angle = end_angle

    # Add relay number in a rectangle at the top of the disk (for multi-route case)
    relay_text = str(relay)
    relay_fs = 17
    rect_width = 14 + (len(relay_text) - 1) * 10  # Dynamic width based on text length
    rect_height = 15
    rect_x = center_x - rect_width / 2
    rect_y = center_y - radius + 5

    drawing.append(draw.Rectangle(rect_x, rect_y, rect_width, rect_height, fill="white", stroke_width=1, stroke="black"))
    drawing.append(
        draw.Text(text=relay_text, font_size=relay_fs, x=center_x, y=rect_y + rect_height / 2 + 1, center=0.5, fill="black", font_family="DejaVu Sans")
    )


def generate_svg_for_relay(relay, group, **kwargs):
    """
    Generates an SVG drawing for a specific relay group.

    Args:
        relay (str): Identifier for the relay group.
        group (list of dicts): Data for the specific relay group.
        **kwargs: Keyword arguments for customizing the chart. Acceptable keys are 'radius',
                  'title_fs', 'grade_fs', 'setter_fs'.

    Returns:
        str: An SVG formatted string representing the generated drawing.
    """
    # Extract parameters with defaults
    radius = kwargs.get("radius", constants.RADIUS)
    title_fs = kwargs.get("title_fs", constants.TITLE_FS)
    grade_fs = kwargs.get("grade_fs", constants.GRADE_FS)
    setter_fs = kwargs.get("setter_fs", constants.SETTER_FS)

    # Create a new SVG drawing
    d = draw.Drawing(width=210, height=297, origin="top-left", displayInline=False)

    # Add a title to the SVG
    relay_name = f"Relais {relay}"
    d.append(draw.Text(text=relay_name, font_size=title_fs, x=105, y=30, center=0.5, valign="top", font_family="DejaVu Sans"))

    # Draw the pie chart
    add_pie_chart_to_svg(
        d,
        group,
        center_x=105,
        center_y=150,
        radius=radius,
        grade_fs=grade_fs,
        setter_fs=setter_fs,
        relay=relay,
    )

    # Return SVG as a string
    return d.as_svg()
