import pandas as pd

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
        pd.DataFrame: A pandas DataFrame containing processed data, specifically the columns 'Relais', 'Cotation',
        'Ouvreur', and 'Couleur'.
    """
    # Read CSV file from StringIO object
    data = pd.read_csv(csv_string_io)

    # Validate required columns
    required_columns = {"Relais", "Couleur", "Cotation", "Ouvreur"}
    if not required_columns.issubset(data.columns):
        missing_columns = required_columns - set(data.columns)
        raise ValueError(f"CSV data is missing the following required columns: {missing_columns}")

    # Process 'Couleur' column using the process_color function from utils
    data["Couleur"] = data["Couleur"].apply(process_color)

    # Extract relevant columns
    relevant_data = data[["Relais", "Cotation", "Ouvreur", "Couleur"]]

    return relevant_data
