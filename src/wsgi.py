import base64
import csv
import io
import logging
import os

from flask import Flask, make_response, request

import climbing_route_chart as crc

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

DEBUG = True
BASE_DIRECTORY = "/app"
DEFAULT_PORT = "8080"


def load_html(filename):
    """
    Loads and returns the content of an HTML file from the base directory.

    Args:
        filename (str): The name of the HTML file to load.

    Returns:
        str: The content of the HTML file.

    Raises:
        FileNotFoundError: If the specified file does not exist.
    """
    file_path = f"{BASE_DIRECTORY}/{filename}"
    with open(file_path, "r") as file:
        return file.read()


def parse_and_validate_csv(text):
    """
    Parses a CSV string, validates its format and headers, and converts it to a standard CSV format if necessary.

    This function checks for a specific set of required headers and validates the number of columns in each row.
    It supports both comma-separated and tab-separated values and will convert tab-separated values to comma-separated
    values if needed.

    Args:
        text (str): The CSV string to parse and validate.

    Returns:
        str: The original or converted CSV string in comma-separated format.

    Raises:
        ValueError: If the CSV header is missing, incorrect, or if any row does not contain the correct number of
        values.
    """
    # Determine delimiter (tab or comma)
    delimiter = "\t" if "\t" in text else ","

    # Read the content using csv.reader
    reader = csv.reader(io.StringIO(text), delimiter=delimiter)

    # Convert to list for easier processing
    rows = list(reader)

    # Check for required headers
    required_headers = ["Relais", "Couleur", "Cotation", "Ouvreur"]
    if rows[0] != required_headers:
        raise ValueError("CSV header missing or incorrect on line 1")

    # Validate each row
    for index, row in enumerate(rows, start=1):  # Start counting from 1
        if len(row) != len(required_headers) and index > 0:  # Skip the header row for this check
            raise ValueError(f"CSV row on line {index} does not contain the correct number of values")

    # If tab-delimited, convert to CSV
    if delimiter == "\t":
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerows(rows)
        return output.getvalue()

    return text  # Return original text if already in CSV format


@app.route("/", methods=["GET", "POST"])
def climb_routes():
    """
    Flask route to handle climbing routes form submission and display.

    - If the request method is GET, it renders and returns an HTML form for input.
    - If the request method is POST, it processes the submitted form data to generate and return a PDF chart of
      climbing routes.

    Uses the `parse_and_validate_csv` function to validate the input data and the `climbing_route_chart` library
    to generate a PDF chart.

    Returns:
        str or werkzeug.wrappers.response.Response: The HTML form content as a string for GET requests
        or a PDF response for POST requests.

    Raises:
        Exception: General exception catch-all for errors during form processing or PDF generation.
    """
    if request.method == "GET":
        logging.info("Rendering form")
        # Load and return the HTML form
        html_content = load_html("form.html")
        return html_content

    elif request.method == "POST":
        logging.info("Processing form")
        try:
            textarea_content = request.form.get("message", "")

            # Parse, validate, and possibly convert the textarea content to CSV
            csv_string = parse_and_validate_csv(textarea_content)

            # Prepare parameters for chart generation
            chart_params = {"title_fs": 14, "grade_fs": 18, "setter_fs": 8, "radius": 69.5}

            # Generate PDF using the climbing_route_chart library
            pdf_stream = crc.generate_climbing_route_charts(csv_string, chart_params)

            if pdf_stream:
                logging.info("PDF rendered")
                pdf_base64 = base64.b64encode(pdf_stream.getvalue()).decode("utf-8")
                response = make_response(base64.b64decode(pdf_base64))
                response.headers.set("Content-Type", "application/pdf")
                response.headers.set("Content-Disposition", 'attachment; filename="etiquettes.pdf"')
                return response
            else:
                logging.info("An error occured")
                raise Exception("Failed to generate the chart.")
        except Exception as e:
            return "Internal Server Error: " + str(e), 500


if __name__ == "__main__":
    # Scaleway's system will inject a PORT environment variable on which your application should start the server.
    port_env = os.getenv("PORT", DEFAULT_PORT)
    port = int(port_env)
    app.run(debug=DEBUG, host="0.0.0.0", port=port)
