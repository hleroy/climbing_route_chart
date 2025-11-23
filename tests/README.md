# Tests

This directory contains test scripts for the climbing route chart generator.

## Visual Tests

### test_gradient_text_colors.py

Generates a comprehensive visual test for gradient text color determination.

**Purpose**: Validates that text overlaid on gradient backgrounds (used in "MARBREE" routes) uses appropriate text color (black or white) for readability.

**How it works**:
- Generates 158+ test cases with various 2-color and 3-color gradient combinations
- For each gradient, calculates the interpolated middle color
- Determines text color based on the middle color's luminance
- Outputs an SVG file showing all test cases for visual inspection

**Usage**:
```bash
# From the root directory, with venv activated
source venv/bin/activate
cd tests
python3 test_gradient_text_colors.py
```

**Output**: `gradient_text_color_test.svg` - Open in any web browser to review the results

**What to look for**: Text should be clearly readable on all gradient backgrounds. If you find any cases where text is hard to read, the luminance threshold in `utils.is_dark_color()` may need adjustment.
