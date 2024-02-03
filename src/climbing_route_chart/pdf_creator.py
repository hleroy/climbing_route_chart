import io

import cairosvg
import PyPDF2


def generate_pdf_from_svgs(svg_list):
    """Generates a multi-page PDF document from a list of SVG strings.

    This function converts each SVG string in the provided list to a PDF page using CairoSVG.
    These pages are then combined into a single PDF document using PyPDF2. The generated PDF is
    intended to be in A4 format with a resolution of 300 DPI.

    Args:
        svg_list (list of str): A list of SVG-formatted strings to be converted to PDF.

    Returns:
        io.BytesIO: A byte stream containing the generated multi-page PDF document.
    """
    pdf_writer = PyPDF2.PdfWriter()
    pdf_stream = io.BytesIO()

    for svg in svg_list:
        svg_bytes = cairosvg.svg2pdf(
            bytestring=svg.encode("utf-8"),
            dpi=300,
            output_width=2480,  # A4 width in pixels at 300 DPI
            output_height=3508,  # A4 height in pixels at 300 DPI
        )
        svg_stream = io.BytesIO(svg_bytes)
        pdf_reader = PyPDF2.PdfReader(svg_stream)
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)

    pdf_writer.write(pdf_stream)
    pdf_stream.seek(0)
    return pdf_stream
