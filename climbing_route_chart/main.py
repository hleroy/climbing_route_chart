import io

from .csv_processor import process_csv
from .pdf_creator import generate_pdf_from_svgs
from .svg_generator import generate_svg_for_relay


def generate_climbing_route_charts(csv_string, params=None):
    """Generates a PDF document containing pie charts for indoor climbing routes from CSV data.

    This function reads CSV data, processes it, and generates a multi-page PDF document. Each page of the PDF
    contains a pie chart representing the distribution of climbing routes for a particular relay. The charts
    illustrate route grades and associated route setters with varying colors.

    In case of an error during processing, the function will print an error message and return `None`.

    Args:
        csv_string (str): A string containing CSV formatted data.
        params (dict, optional): A dictionary of parameters to customize the charts.
            Possible keys include 'title_fs', 'grade_fs', 'setter_fs', and 'radius'.
            If None, default values are used. Defaults to None.

    Returns:
        io.BytesIO or None: A byte stream containing the generated PDF document, or `None` if an
        error occurred during processing.
    """
    try:
        # Ensure params is a dictionary
        if params is None:
            params = {}

        csv_string_io = io.StringIO(csv_string)
        climbing_data = process_csv(csv_string_io)

        # Group data by 'Relais'
        grouped_data = climbing_data.groupby("Relais")

        # Generate SVG for each 'Relais' group using the parameters
        svg_list = [generate_svg_for_relay(relay, group, **params) for relay, group in grouped_data]

        # Generate a multi-page PDF file with all the SVGs
        pdf_stream = generate_pdf_from_svgs(svg_list)

        return pdf_stream

    except Exception as e:
        print("An error occurred while generating the charts.")
        print(e)
        return None
