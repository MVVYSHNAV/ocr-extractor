import pytesseract
import easyocr
import numpy as np
from PIL import Image
from ocrapp.extractors.base import BaseExtractor
from ocrapp.utils import is_pdf, pdf_to_images

class PytesseractExtractor(BaseExtractor):
    @property
    def name(self) -> str:
        return "pytesseract"
        
    def extract(self, file_path: str) -> str:
        # Check if tesseract is installed
        import shutil
        if not shutil.which("tesseract"):
            raise FileNotFoundError("Tesseract is not installed on the system.")
            
        images = []
        if is_pdf(file_path):
            images = pdf_to_images(file_path)
        else:
            images = [Image.open(file_path)]
            
        full_text = []
        for img in images:
            text = pytesseract.image_to_string(img)
            full_text.append(text)
            
        return "\n".join(full_text)

import logging
# Suppress easyocr warning
logging.getLogger("easyocr.easyocr").setLevel(logging.ERROR)

class EasyOCRExtractor(BaseExtractor):
    def __init__(self):
        super().__init__()
        # Initialize easyocr reader once
        self.reader = easyocr.Reader(['en'], gpu=False)  # Setting gpu=False to avoid dependency issues across different machines
        
    @property
    def name(self) -> str:
        return "easyocr"
        
    def extract(self, file_path: str) -> str:
        images = []
        if is_pdf(file_path):
            images = pdf_to_images(file_path)
        else:
            images = [Image.open(file_path)]
            
        full_text = []
        for img in images:
            # easyocr requires numpy array
            img_np = np.array(img)
            result = self.reader.readtext(img_np, detail=0)
            full_text.append(" ".join(result))
            
        return "\n".join(full_text)
