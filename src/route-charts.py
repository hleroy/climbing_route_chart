#!/usr/bin/env python3
"""
Climbing Route Chart Generator

This script produces SVG documents displaying pie charts for indoor climbing routes based on a CSV input. Each chart
corresponds to a climbing relay, illustrating the distribution of route grades and the associated route setters. The
charts use varying colors to differentiate between grades. The output is a PDF file suitable for printing in A4 format.

Usage:
    ./route-charts.py -i <input_file.csv> [-o <output_file.pdf>]

Arguments:
    -i, --input (str): Mandatory filepath to the CSV containing climbing routes data.
    -o, --output (str): Optional destination filepath for the generated PDF file, default is 'charts.pdf'.
    --title_fs (int): Optional font size for the title, default is 14.
    --grade_fs (int): Optional font size for the grade, default is 18.
    --setter_fs (int): Optional font size for the route setter, default is 8.
    --radius (float): Optional radius of the pie charts in mm, default is 69.5.

Author:
    Hervé Le Roy
"""

import argparse
import csv
import os

import climbing_route_chart as crc

sample_csv_data = """Relais,Couleur,Cotation,Ouvreur
1,BLEUE,4b,MAT
1,VIOLETTE,6b,SOLVEIG
1,MARBREE (JAUNE / NOIRE),5a+,MAT
1,MARBREE (VERTE/ BLANCHE),6b+,MAT
2,ROUGE,6a+,MAT
2,ORANGE,4c,MAT
2,VERTE,5b,SOLVEIG
2,JAUNE,5c,MANU
3,BLANCHE,6a,TANGUY
3,MAUVE,6b,MAT
3,JAUNE FLUO,4c,?
3,MARBREE (BLANCHE / BLEUE),5a+,SOREN
4,BLEUE,4c,TANGUY
4,ROUGE,5a,ELIOTT"""  # CSV data as string


def parse_arguments():
    """Parses command line arguments and returns the parsed arguments.

    This function defines and handles the command line arguments for the script. It requires
    the input CSV file path and allows optional arguments for the output PDF file path, title font size,
    grade font size, setter font size, and pie chart radius.

    Returns:
        argparse.Namespace: An object containing parsed command line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Generate a multi-page PDF document of color pie charts for climbing routes grades. "
        "The input CSV file should have columns for 'Relais' (relay), 'Couleur' (color), "
        "'Cotation' (grade), and 'Ouvreur' (route setter)."
    )
    # Mandatory input file argument
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        required=False,
        help="Filepath to the CSV containing climbing routes data",
    )
    # Optional output file argument with a shorter flag
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="charts.pdf",
        help="Destination filepath for the generated PDF file, default charts.pdf",
    )
    parser.add_argument("--title_fs", type=int, help="Font size for the title (default: 14).")
    parser.add_argument("--grade_fs", type=int, help="Font size for the grade (default: 18).")
    parser.add_argument("--setter_fs", type=int, help="Font size for the route setter (default: 8).")
    parser.add_argument("--radius", type=float, help="Radius of the pie charts in mm (default: 69.5).")
    return parser.parse_args()


def validate_csv_file(file_path):
    """Validates the presence and format of the input CSV file.

    Checks if the file exists at the given path and contains the required columns:
    'Relais', 'Couleur', 'Cotation', and 'Ouvreur'.

    Args:
        file_path (str): The file path for the input CSV file.

    Returns:
        bool: True if the file is valid, False otherwise.
    """
    required_columns = {"Relais", "Couleur", "Cotation", "Ouvreur"}

    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"Error: The specified input file '{file_path}' does not exist.")
        return False

    # Check if the file contains the required columns
    try:
        with open(file_path, mode="r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            columns = set(reader.fieldnames)

            if not required_columns.issubset(columns):
                missing_columns = required_columns - columns
                print(f"Error: The input file is missing the following required columns: {missing_columns}")
                return False
    except Exception as e:
        print(f"Error reading the CSV file: {e}")
        return False

    return True


def prepare_chart_parameters(args):
    """Extracts and prepares chart parameters from the parsed arguments.

    Processes the command line arguments to create a dictionary of chart parameters, excluding any arguments
    that were not provided (i.e., are None).

    Args:
        args (argparse.Namespace): The parsed command line arguments.

    Returns:
        dict: A dictionary of chart parameters with None values removed.
    """
    chart_params = {
        "title_fs": args.title_fs,
        "grade_fs": args.grade_fs,
        "setter_fs": args.setter_fs,
        "radius": args.radius,
    }
    # Remove None values
    return {k: v for k, v in chart_params.items() if v is not None}


def main():
    """The main function of the script.

    Orchestrates the overall process of generating the climbing route charts. It parses command line arguments,
    validates the CSV file, reads the CSV data, prepares chart parameters, and generates a PDF using the
    climbing_route_charts package. Finally, it writes the PDF stream to the specified output file.
    """
    # Parse arguments
    args = parse_arguments()

    try:
        # Handle absence of input
        if args.input is None:
            print("No input was provided: a chart is being generated with sample data.")
            csv_data = sample_csv_data
            args.output = args.output if args.input is not None else "sample_data_chart.pdf"
        else:
            # Validate csv file
            if not validate_csv_file(args.input):
                exit(1)

            # Open csv file
            with open(args.input, "r") as csv_file:
                csv_data = csv_file.read()

        # Prepare parameters for chart generation
        chart_params = prepare_chart_parameters(args)

        # Use the climbing_route_charts package to generate the PDF
        pdf_stream = crc.generate_climbing_route_charts(csv_data, chart_params)

        if pdf_stream:
            # Write the PDF stream to the output file
            with open(args.output, "wb") as output_file:
                output_file.write(pdf_stream.getvalue())
            print(f"Successfully generated the climbing route chart: {args.output}")
        else:
            print("Failed to generate the chart.")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
