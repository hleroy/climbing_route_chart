#!/usr/bin/env python3
"""
Test script to generate visual examples of text color determination for gradients.
Creates an SVG with multiple gradient examples showing text overlay.
"""

import sys
import os

# Add src to path to import the module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import drawsvg as draw
from climbing_route_chart.utils import interpolate_gradient_middle_color, is_dark_color

# Define test gradients with various color combinations
test_gradients = []

# Common colors from the application
common_colors = {
    'White': '#FFFFFF',
    'Black': '#000000',
    'Red': '#FF0000',
    'Blue': '#0000FF',
    'Green': '#00FF00',
    'Yellow': '#FFFF00',
    'Orange': '#FFA500',
    'Purple': '#800080',
    'Pink': '#FFC0CB',
    'Brown': '#8B4513',
    'Gray': '#808080',
    'Cyan': '#00FFFF',
    'Magenta': '#FF00FF',
    'Lime': '#00FF00',
    'Navy': '#000080',
    'Teal': '#008080',
    'Olive': '#808000',
    'Maroon': '#800000',
}

color_list = list(common_colors.items())

# Generate 2-color gradients
for i in range(len(color_list)):
    for j in range(i + 1, len(color_list)):
        name1, hex1 = color_list[i]
        name2, hex2 = color_list[j]
        test_gradients.append({
            'colors': [hex1, hex2],
            'name': f'{name1} → {name2}'
        })

# Generate some 3-color gradients
three_color_combos = [
    (['#FF0000', '#FFFF00', '#0000FF'], 'Red → Yellow → Blue'),
    (['#000000', '#808080', '#FFFFFF'], 'Black → Gray → White'),
    (['#00FF00', '#FFFF00', '#FF0000'], 'Green → Yellow → Red'),
    (['#0000FF', '#FF00FF', '#FF0000'], 'Blue → Magenta → Red'),
    (['#FFFFFF', '#FFA500', '#000000'], 'White → Orange → Black'),
]

for colors, name in three_color_combos:
    test_gradients.append({'colors': colors, 'name': name})

print(f"Generating {len(test_gradients)} gradient test cases...")

# Create SVG
box_width = 200
box_height = 60
boxes_per_row = 5
margin = 10

rows = (len(test_gradients) + boxes_per_row - 1) // boxes_per_row
svg_width = boxes_per_row * (box_width + margin) + margin
svg_height = rows * (box_height + margin) + margin + 50

d = draw.Drawing(svg_width, svg_height, origin='top-left')

# Add title
d.append(draw.Text(
    'Gradient Text Color Test - Black or White text based on interpolated middle color',
    font_size=16,
    x=svg_width / 2,
    y=25,
    center=0.5,
    font_family='DejaVu Sans',
    fill='black'
))

# Generate each test case
for idx, test_case in enumerate(test_gradients):
    row = idx // boxes_per_row
    col = idx % boxes_per_row

    x = margin + col * (box_width + margin)
    y = 50 + margin + row * (box_height + margin)

    colors = test_case['colors']
    name = test_case['name']

    # Create gradient
    gradient = draw.LinearGradient(x, y, x + box_width, y)
    for i, color in enumerate(colors):
        offset = i / (len(colors) - 1) if len(colors) > 1 else 0
        gradient.add_stop(offset, color)

    # Draw rectangle with gradient
    d.append(draw.Rectangle(x, y, box_width, box_height, fill=gradient, stroke='black', stroke_width=1))

    # Calculate middle color and text color
    middle_color = interpolate_gradient_middle_color(colors)
    text_color = "white" if is_dark_color(middle_color) else "black"

    # Draw text overlay
    text_y = y + box_height / 2 - 10
    d.append(draw.Text(
        name,
        font_size=11,
        x=x + box_width / 2,
        y=text_y,
        center=0.5,
        fill=text_color,
        font_family='DejaVu Sans',
        font_weight='bold'
    ))

    # Show middle color hex
    d.append(draw.Text(
        f'Mid: {middle_color}',
        font_size=9,
        x=x + box_width / 2,
        y=text_y + 15,
        center=0.5,
        fill=text_color,
        font_family='DejaVu Sans'
    ))

    # Show text color choice
    d.append(draw.Text(
        f'Text: {text_color}',
        font_size=9,
        x=x + box_width / 2,
        y=text_y + 27,
        center=0.5,
        fill=text_color,
        font_family='DejaVu Sans'
    ))

# Save SVG
output_file = 'gradient_text_color_test.svg'
d.save_svg(output_file)
print(f"✓ Generated test file: {output_file}")
print(f"  Open this file in a browser to review the text color choices.")
