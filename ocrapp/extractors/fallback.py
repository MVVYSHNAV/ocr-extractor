import textract
from ocrapp.extractors.base import BaseExtractor

class TextractExtractor(BaseExtractor):
    @property
    def name(self) -> str:
        return "textract"
        
    def extract(self, file_path: str) -> str:
        # textract returns bytes
        raw_bytes = textract.process(file_path)
        return raw_bytes.decode('utf-8', errors='ignore')
