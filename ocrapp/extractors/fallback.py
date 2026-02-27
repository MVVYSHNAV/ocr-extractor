import textract
from ocrapp.extractors.base import BaseExtractor

class TextractExtractor(BaseExtractor):
    @property
    def name(self) -> str:
        return "textract"
        
    def extract(self, file_path: str) -> str:
        # Textract throws an error explicitly for pdfs but its error message falsely claims it supports them
        if file_path.lower().endswith('.pdf'):
            raise ValueError("Textract does not natively support PDF parsing without pdftotext installed. Using built-in PDF extractors instead.")
            
        # textract returns bytes
        raw_bytes = textract.process(file_path)
        return raw_bytes.decode('utf-8', errors='ignore')
