# tests/utils.py
from io import BytesIO
from reportlab.pdfgen import canvas

def generate_dummy_pdf(text="Hello, World!"):
    """Generate a simple PDF in memory with some text."""
    buffer = BytesIO()
    c = canvas.Canvas(buffer)
    c.drawString(100, 750, text)
    c.save()
    buffer.seek(0)
    return buffer

def generate_empty_pdf():
    """Generate an empty PDF in memory."""
    buffer = BytesIO()
    c = canvas.Canvas(buffer)
    c.save()
    buffer.seek(0)
    return buffer
