import os
import mimetypes
import logging
from typing import Dict, Any, List

from ocrapp.scoring.scorer import TextScorer
from ocrapp.extractors.pdf_extractors import DoclingExtractor, PdfPlumberExtractor, PyMuPDFExtractor
from ocrapp.extractors.ocr_extractors import PytesseractExtractor, EasyOCRExtractor
from ocrapp.extractors.doc_extractors import DocxExtractor, HtmlExtractor

logger = logging.getLogger(__name__)

class DocumentExtractor:
    """
    Main orchestrator that selects appropriate extractors based on file type,
    executes them, scores the results, and returns the best extraction.
    """
    def __init__(self):
        self.scorer = TextScorer()
        
        # Initialize extractors
        logger.info("Initializing extractors...")
        self.docling = DoclingExtractor()
        self.pdfplumber = PdfPlumberExtractor()
        self.pymupdf = PyMuPDFExtractor()
        
        self.pytesseract = PytesseractExtractor()
        self.easyocr = EasyOCRExtractor()
        
        self.docx = DocxExtractor()
        self.html = HtmlExtractor()
        logger.info("Extractors initialized successfully.")

    def _get_extractors_for_file(self, file_path: str) -> List[Any]:
        ext = os.path.splitext(file_path)[1].lower()
        mime, _ = mimetypes.guess_type(file_path)
        
        extractors = []
        
        if ext == '.pdf' or mime == 'application/pdf':
            # Try PDF-specific first
            extractors.extend([self.docling, self.pymupdf, self.pdfplumber])
            # Also add OCR as fallback if PDF is scanned
            extractors.extend([self.pytesseract, self.easyocr])
            
        elif ext in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp'] or (mime and mime.startswith('image/')):
            # Image files
            extractors.extend([self.pytesseract, self.easyocr])
            
        elif ext == '.docx' or mime == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            extractors.append(self.docx)
            
        elif ext in ['.html', '.htm'] or mime == 'text/html':
            extractors.append(self.html)
        
        return extractors

    def process(self, file_path: str, extractor_name: str = "Auto-Select") -> Dict[str, Any]:
        """
        Process a file and return the best extraction result, or the explicitly requested one.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        all_extractors = [
            self.docling, self.pdfplumber, self.pymupdf,
            self.pytesseract, self.easyocr,
            self.docx, self.html
        ]
            
        if extractor_name and extractor_name != "Auto-Select":
            # Find the specific extractor requested
            extractors = [e for e in all_extractors if e.name == extractor_name]
            if not extractors:
                raise ValueError(f"Unknown extractor: {extractor_name}")
        else:
            # Auto-route
            extractors = self._get_extractors_for_file(file_path)
        
        results = []
        
        for extractor in extractors:
            logger.info(f"Attempting extraction with [{extractor.name}]...")
            try:
                text = extractor.extract(file_path)
                score = self.scorer.score(text)
                results.append({
                    "source": extractor.name,
                    "score": score,
                    "text": text
                })
                logger.info(f"[{extractor.name}] Score: {score:.2f}")
            except Exception as e:
                logger.error(f"[{extractor.name}] Failed: {str(e)}")
                # We do not discard failed extractors silently but rather log them and skip scoring.
                results.append({
                    "source": extractor.name,
                    "score": -1.0,
                    "text": "",
                    "error": str(e)
                })
                
        # Filter successful ones
        valid_results = [r for r in results if r["score"] >= 0]
        
        if not valid_results:
            return {
                "source": "None",
                "score": 0.0,
                "text": "",
                "debug": results,
                "error": "All extractors failed."
            }
            
        # Select best
        best_result = max(valid_results, key=lambda x: x["score"])
        
        return {
            "source": best_result["source"],
            "score": best_result["score"],
            "text": best_result["text"],
            "debug": results
        }
