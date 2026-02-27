import docx
from bs4 import BeautifulSoup
from ocrapp.extractors.base import BaseExtractor

class DocxExtractor(BaseExtractor):
    @property
    def name(self) -> str:
        return "python-docx"
        
    def extract(self, file_path: str) -> str:
        doc = docx.Document(file_path)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])

class HtmlExtractor(BaseExtractor):
    @property
    def name(self) -> str:
        return "beautifulsoup4"
        
    def extract(self, file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, "html.parser")
            return soup.get_text(separator='\n', strip=True)
