import fitz
import pdfplumber
from docling.document_converter import DocumentConverter
from ocrapp.extractors.base import BaseExtractor

class PyMuPDFExtractor(BaseExtractor):
    @property
    def name(self) -> str:
        return "PyMuPDF"
        
    def extract(self, file_path: str) -> str:
        text = []
        with fitz.open(file_path) as doc:
            for page in doc:
                text.append(page.get_text())
        return "\n".join(text)

class PdfPlumberExtractor(BaseExtractor):
    @property
    def name(self) -> str:
        return "pdfplumber"
        
    def extract(self, file_path: str) -> str:
        text = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text.append(extracted)
        return "\n".join(text)

class DoclingExtractor(BaseExtractor):
    def __init__(self):
        super().__init__()
        # The document converter initializes the models upon startup if necessary.
        self.converter = DocumentConverter()
        
    @property
    def name(self) -> str:
        return "docling"
        
    def extract(self, file_path: str) -> str:
        result = self.converter.convert(file_path)
        return result.document.export_to_markdown()
