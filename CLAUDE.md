# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Climbing Route Chart Generator is a Python application that generates pie chart graphics to visualize indoor climbing routes. It accepts CSV input with route data (relay, color, grade, setter) and produces PDF charts suitable for printing climbing gym labels in A4 format.

The tool can be used in three ways:
1. CLI (command line)
2. Flask web application
3. Docker container

## Core Architecture

### Main Package: `src/climbing_route_chart/`

The application follows a pipeline architecture:

1. **CSV Processing** (`csv_processor.py`): Parses and validates CSV data, converts color names to hex codes
2. **SVG Generation** (`svg_generator.py`): Creates pie chart SVG graphics using drawSvg library
3. **PDF Creation** (`pdf_creator.py`): Converts SVG graphics to multi-page PDF using cairosvg and PyPDF2
4. **Main Entry Point** (`main.py`): Orchestrates the pipeline via `generate_climbing_route_charts()` function

### Color Processing

The `utils.py` module handles color conversion:
- Maps French/English color names to hex codes via `COLOR_MAPPING` in `constants.py`
- Supports "MARBREE" (marbled) colors with gradient fills: `MARBREE (COLOR1 / COLOR2)`
- Accepts direct hex codes (e.g., `#FF0000`)
- Defaults to gray (`#808080`) for unknown colors

### Entry Points

- **CLI**: `src/route-charts.py` - Command-line tool with argparse
- **Web App**: `src/wsgi.py` - Flask application with Gunicorn
  - Main route `/` - Form submission and PDF generation
  - `/colors` route - Displays available color mappings

## CSV Format

Required columns: `Relais`, `Couleur`, `Cotation`, `Ouvreur`

Example:
```
Relais,Couleur,Cotation,Ouvreur
1,BLEUE,4b,MAT
1,MARBREE (JAUNE / NOIRE),5a+,MAT
```

## Development Commands

### Setup
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac: or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### CLI Usage
```bash
cd src
./route-charts.py -i <input_file.csv> [-o <output_file.pdf>]
./route-charts.py --help  # See all options (title_fs, grade_fs, setter_fs, radius)
```

### Run Web Application Locally
```bash
cd src
python wsgi.py  # Runs on port 8080 by default
```

### Docker
```bash
docker build -t climb-routes .
docker run -p 8080:8080 climb-routes
```

### Code Quality Tools
Configured in `pyproject.toml`:
- **Black**: Line length 119, target Python 3.11
- **isort**: Profile "black", line length 119
- **PyLint**: Max line length 119

## Key Dependencies

- `drawSvg` - SVG generation for pie charts
- `cairosvg` - SVG to PDF conversion
- `PyPDF2` - PDF manipulation/merging
- `Flask` - Web interface
- `gunicorn` - WSGI server

## Important Notes

- The application groups routes by "Relais" number and creates one PDF page per relay
- Default pie chart radius is 69.5mm (configurable)
- Font sizes are customizable via CLI flags or chart_params dictionary
- Web app runs on port 8080 (configurable via PORT environment variable)
- Charts are optimized for A4 format at 300 DPI (2480x3508 pixels)
