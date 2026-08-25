import pymupdf
from PIL import Image
import io

def get_page_text(page):
    """Return the text layer of a page, if it has one."""
    return page.get_text()

def get_page_image(page, dpi=300):
    """Render a page to a PIL image (used when OCR fallback is needed)."""
    pix = page.get_pixmap(dpi=dpi)
    return Image.open(io.BytesIO(pix.tobytes("png")))

def open_pdf(pdf_path):
    return pymupdf.open(pdf_path)