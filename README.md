Climbing Route Chart Generator
==============================

[Version française](README.fr.md)

## Overview

__Climbing Route Chart Generator__ is a Python application designed for generating visual pie charts of indoor climbing routes. These charts are produced from CSV input, illustrating the distribution of route grades and the associated route setters. The tool is ideal for climbing gyms who wish to visualize route distributions in an easy-to-understand format.

![Sample chart](screenshot.png)

## Installation

To set up Climbing Route Chart Generator, follow these steps:

1. Create a virtual environment in a folder named "env":
   ```bash
   python -m venv env
   ```
2. Activate the virtual environment:
   - On Windows:
     ```bash
     .\env\Scripts\activate
     ```
   - On Unix or MacOS:
     ```bash
     source env/bin/activate
     ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the script with the following command:

```bash
./route-charts.py -i <input_file.csv> [-o <output_file.pdf>]
```

### Arguments

Refer to the output of `./route-charts.py --help` for a list of all optional arguments.

## Input Format

The input should be a CSV file with the following columns:

- Relais
- Couleur
- Cotation
- Ouvreur

## License

This project is unlicensed and free for public domain use. For more details, see [UNLICENSE](UNLICENSE).
