import csv

from .utils import process_color


def process_csv(csv_string_io):
    """Reads and processes CSV data from a StringIO object for chart generation.

    This function reads climbing route data from a CSV-formatted string and processes it. It checks for
    the presence of required columns and converts color names in the 'Couleur' column to their corresponding
    hex codes using the `process_color` function. It then extracts only the relevant columns for chart
    generation.

    Args:
        csv_string_io (io.StringIO): A StringIO object containing CSV-formatted data of climbing routes.

    Raises:
        ValueError: If the CSV data is missing one or more required columns or if the CSV is malformed.

    Returns:
        List of Dicts: Each dict contains processed data for a row, specifically the columns 'Relais', 'Cotation',
        'Ouvreur', and 'Couleur'.
    """
    reader = csv.DictReader(csv_string_io)

    # Validate required columns
    required_columns = {"Relais", "Couleur", "Cotation", "Ouvreur"}
    if not required_columns.issubset(reader.fieldnames):
        missing_columns = required_columns - set(reader.fieldnames)
        raise ValueError(f"CSV data is missing the following required columns: {missing_columns}")

    # Process data
    processed_data = []
    for row in reader:
        # Convert color names to hex codes
        row["Couleur"] = process_color(row["Couleur"])

        # Extract relevant columns and add to processed data
        processed_data.append({col: row[col] for col in required_columns})

    return processed_data
