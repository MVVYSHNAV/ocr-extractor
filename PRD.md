# Product Requirements Document (PRD): Smart Document Text Extraction App

## 1. Product Overview
The **Smart Document Text Extraction App** is an intelligent, autonomous pipeline for unstructured document parsing. Target users (Platform Engineers, MLOps, Data Scientists) frequently encounter messy documents containing mixed formatted text, tables, and images. Single-library extractions fail frequently on diverse data structures. This application dynamically routes doc types to multiple state-of-the-art libraries, evaluates the raw outputs autonomously against precision heuristics, and outputs the absolute highest-fidelity text.

## 2. Target Audience
* **Data Engineers / Analysts:** Need reliable pure-text representations of vendor formats.
* **Automation Developers:** Feeding unstructured documents to LLMs via RAG pipelines.
* **Platform Engineers:** Need a seamless interface bypassing repetitive OCR deployment testing.

## 3. Product Features & Capabilities

### 3.1. Universal File Ingestion
- Auto-detect formats via extension and MIME-type validation.
- **Native Support:** `.pdf`, `.png`, `.jpg`, `.jpeg`, `.docx`, `.html`.
- **Fallback Support:** Leverages `textract` to brute-force unsupported formats (e.g. `.rtf`, `.msg`).

### 3.2. Extraction Orchestrator
- Does **not** blindly merge text strings (prevents data corruption and duplication).
- Runs competitive engine execution.
- **Engines integrated:**
  - Standard Readers: `PyMuPDF`, `pdfplumber`, `python-docx`, `beautifulsoup4`.
  - Machine Learning & OCR: `Docling` (Layout-aware NLP), `easyocr`, `pytesseract`.

### 3.3. Accuracy Scoring Algorithm (The "Scorer")
The core IP of the tool. Computes a quantitative Confidence Score dynamically evaluating:
- **Length Normalization**: Eliminates naive biases toward noisy heavy outputs.
- **Garbage & Symbol Ratio**: Strictly penalizes extraction strings overwhelmed by unusual or non-alphanumeric unicode mappings (a symptom of failed OCR blocks).
- **Word-to-Character Density**: Penalizes fused string outputs `(likethisexample)` or heavily fragmented character outputs `(l i k e t h i s)`.
- **Formatting Disturbance**: Penalizes excessive trailing whitespaces and consecutive newlines masking missing data.
- **Language Detection**: Rewards strings confidentially returning structured English grammar probabilities.

### 3.4. Streamlit User Interface
- **Drag-And-Drop Portal**: Clean `.st-file-uploader` UI targeting non-technical testers.
- **Live Benchmarking**: Asynchronous processing spinners detailing real-time orchestration behavior.
- **Visual Confidence Deck**: Explictly displays `"Best Extractor"` along with its score and time-to-execute.
- **Visual Debug Metrics**: Shows all tested fallback engines and scores for diagnostic transparency.

### 3.5. Data Export
- Immediate raw text preview box within the web browser.
- Universal `Download as TXT` native functionality.
- One-click `Save to Disk` routing pipeline pushing organized timestamped blobs to the backend `results/` directory.

## 4. Technical Constraints & Non-Goals
* **No Cloud NLP Execution**: Runs 100% locally to comply with highest data-privacy regulations (uses offline `Docling` PyTorch models or local Tesseract runtimes).
* **No Blind Trust in PDF Textual Layers**: Scanned PDFs spoof text layers frequently. The system inherently generates image matrices of PDFs ensuring OCR engines compete fairly against `PyMuPDF`.
* **Graceful Failures Only**: Exception handling guarantees the Orchestrator does not crash if an individual extraction dependency (like Tesseract) is missing in the host system.

## 5. Deployment Specs
- Language: `Python 3.10+`
- Compute: CPU execution viable (EasyOCR enforced `gpu=False`), but highly scales on CUDA/PyTorch integrations.
- Environment: VENV dependent via `requirements.txt`.
