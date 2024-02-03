Climbing Route Chart Generator
==============================

[Version française](README.fr.md)

## Overview

__Climbing Route Chart Generator__ is a Python application designed to generate pie chart graphics to visualize indoor
climbing routes. These charts are produced from a CSV input, illustrating the distribution of the route grades and the
associated setters. The tool is ideal for climbing gym managers to quickly and easily update the labels after a
setting campaign.

![Sample chart](screenshot.png)


## Online tool

The simplest way to use this tool is to use the online version hosted by __Adrénaline Escalade__, a climbing club from Hauts de Seine (92) in France.

[https://etiquettes.adrenaline-escalade.com/](https://etiquettes.adrenaline-escalade.com/)


## Using locally with Docker

This is the simplest option, assuming you already have Docker installed:

      $ docker build -t climb-routes .
      $ docker run -p 8080:8080 climb-routes

Open your browser and navigate to localhost:8080


## Using locally with CLI (command line interface)

### Setup

To set up Climbing Route Chart Generator, follow these steps:

1. Create a virtual environment in a folder named "venv":
   ```bash
   python -m venv venv
   ```
2. Activate the virtual environment:
   - On Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - On Linux or MacOS:
     ```bash
     source venv/bin/activate
     ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

Run the script with the following command:

```bash
cd src
./route-charts.py -i <input_file.csv> [-o <output_file.pdf>]
```

### Arguments

Refer to the output of `./route-charts.py --help` for a list of all optional arguments.

### Input Format

The input should be a CSV file with the following columns:

- Relais
- Couleur
- Cotation
- Ouvreur

## License

This project is unlicensed and free for public domain use. For more details, see [UNLICENSE](UNLICENSE).
