import fitz
from PIL import Image
import os
import mimetypes

def is_pdf(file_path: str) -> bool:
    mime, _ = mimetypes.guess_type(file_path)
    if mime == 'application/pdf':
        return True
    return file_path.lower().endswith(".pdf")

def pdf_to_images(pdf_path: str) -> list[Image.Image]:
    """
    Given a PDF path, renders all pages to PIL Images for OCR processing.
    """
    images = []
    with fitz.open(pdf_path) as doc:
        for page in doc:
            # 200 DPI is usually sufficient for good OCR without being overly slow
            pix = page.get_pixmap(matrix=fitz.Matrix(200/72, 200/72))
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            images.append(img)
    return images
