# Smart Document Text Extraction App

A production-ready Python application that extracts text from various documents (PDF, Scanned PDF, Images, DOCX, HTML) using multiple extraction libraries and intelligently selects the best result based on an accuracy scoring heuristic.

## Core Features
- **Auto-detection**: Dynamically determines the file type (MIME type or extension) and routes it to the appropriate extractors.
- **Accuracy Scoring**: Evaluates the extracted text based on word density, garbage/symbol ratio, OCR noise, and language detection confidence.
- **Multiple Extractors**:
  - PDFs: `docling`, `pdfplumber`, `PyMuPDF`
  - OCR (Images/Scanned PDFs): `pytesseract`, `easyocr`
  - Documents: `python-docx` (DOCX), `beautifulsoup4` (HTML)
- **Graceful Error Handling**: Individual extractor failures do not crash the application.
- **CLI Interface**: User-friendly command-line interface with verbose logging and JSON output support.

## Prerequisites
- Python 3.10+
- `tesseract-ocr` (For pytesseract OCR)
- `poppler-utils` (For pdf to image conversions / pdfplumber)

Ubuntu/Debian installation:
```bash
sudo apt-get install tesseract-ocr poppler-utils
```

## Installation

1. Create a virtual environment and activate it:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install requirements:
```bash
pip install -r requirements.txt
```


```
sudo apt-get update && sudo apt-get install -y tesseract-ocr poppler-utils
```
## Usage

### Command Line Interface (CLI)
You can run the extractor directly via the terminal. Make sure you have activated the virtual environment first.

```bash
# Activate virtual environment
source venv/bin/activate

# Standard execution
python -m ocrapp.cli path/to/document.pdf

# With verbose logging (shows which extractors are executing and their scores)
python -m ocrapp.cli path/to/document.pdf --verbose

# JSON output
python -m ocrapp.cli path/to/document.pdf --json
```

### Streamlit Web Application
You can also run the web interface which provides an easy-to-use drag and drop UI to upload your files, preview text, view the absolute winner and their scores, and easily download and manage text extraction results.

Ensure you are in the application folder and your virtual environment is activated:
```bash
source venv/bin/activate
streamlit run app.py
```
This will launch a local server and give you an address you can open in your browser (typically `http://localhost:8501`).

### Module Import
You can use the `DocumentExtractor` directly in your Python code:

```python
from ocrapp.core.orchestrator import DocumentExtractor

extractor = DocumentExtractor()
result = extractor.process("path/to/document.pdf")

print(f"Best Engine: {result['source']}")
print(f"Confidence: {result['score']}")
print(f"Text: {result['text']}")
```

## Architecture
- **`ocrapp/extractors/`**: Contains the base interface and individual extractor implementations.
  - PDF: `DoclingExtractor`, `PdfPlumberExtractor`, `PyMuPDFExtractor`
  - OCR: `EasyOCRExtractor`, `PytesseractExtractor`
- **`ocrapp/scoring/scorer.py`**: The `TextScorer` class evaluates text length, garbage char ratio, word lengths, language detection, and OCR-specific noise like scattered characters or repetitive newlines.
- **`ocrapp/core/orchestrator.py`**: The `DocumentExtractor` maps files to sensible extraction pipelines (e.g., text PDF vs scanned PDF), scores them, and determines the most accurate output without blindly merging text.
