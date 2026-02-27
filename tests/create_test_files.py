import os
import subprocess
from PIL import Image, ImageDraw, ImageFont

def ensure_dependencies():
    try:
        import docx
    except ImportError:
        subprocess.check_call(["pip", "install", "python-docx"])
        
    try:
        import reportlab
    except ImportError:
        subprocess.check_call(["pip", "install", "reportlab"])

ensure_dependencies()

import docx
from reportlab.pdfgen import canvas

os.makedirs("tests", exist_ok=True)

# 1. Create Text PDF
c = canvas.Canvas("tests/test_text.pdf")
c.drawString(100, 750, "This is a simple text-based PDF.")
c.drawString(100, 730, "Testing PDF extractors like Docling and PyMuPDF.")
c.save()

# 2. Create Image with text
img = Image.new('RGB', (600, 300), color=(255, 255, 255))
d = ImageDraw.Draw(img)
d.text((50, 50), "This is an image containing text.", fill=(0,0,0))
d.text((50, 100), "Testing OCR extractors like pytesseract and easyocr.", fill=(0,0,0))
img.save("tests/test_image.jpg")

# 3. Create Scanned PDF (PDF containing an image)
c2 = canvas.Canvas("tests/test_scanned.pdf")
c2.drawImage("tests/test_image.jpg", 100, 500, width=400, height=200)
c2.save()

# 4. Create DOCX
doc = docx.Document()
doc.add_paragraph("This is a simple DOCX file for testing the python-docx extractor.")
doc.save("tests/test_doc.docx")

# 5. Create HTML
with open("tests/test_html.html", "w") as f:
    f.write("<html><body><h1>Test HTML</h1><p>This is a test HTML file for BeautifulSoup.</p></body></html>")

print("Generated test files successfully.")
