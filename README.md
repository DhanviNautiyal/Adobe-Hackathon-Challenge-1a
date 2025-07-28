# Adobe Hackathon Challenge 1a - PDF Processing Solution

## Overview
This solution extracts document titles and outlines from PDF files with multilingual support and image OCR capabilities.

## Tech Stack
- **Python 3.10**: Core programming language
- **PyMuPDF (fitz)**: PDF text and image extraction
- **Tesseract OCR**: Image text extraction with multilingual support
- **Pillow (PIL)**: Image processing and manipulation
- **langdetect**: Language detection for multilingual support
- **concurrent.futures**: Parallel processing for performance optimization
- **pathlib**: Cross-platform file path handling
- **json**: Output formatting

## Features
- **Multilingual Support**: Hindi, English, Japanese, Arabic, Chinese, Russian, French
- **Image OCR**: Extracts text from images within PDFs
- **Performance Optimized**: Processes 50-page PDFs in under 10 seconds
- **Modular Design**: Uses shared utilities for code reuse

## Setup Instructions

### Prerequisites
1. **Python 3.10** (recommended) or Python 3.8+
2. **Tesseract OCR** (optional, for image text extraction)

### Installation Steps

#### 1. Clone the Repository
```bash
git clone https://github.com/DhanviNautiyal/Adobe-Hackathon-Challenge-1a.git
cd Adobe-Hackathon-Challenge-1a
```

#### 2. Install Tesseract OCR (Optional)
**Windows:**
- Download from: https://github.com/UB-Mannheim/tesseract/wiki
- Add to PATH: `C:\Program Files\Tesseract-OCR`

**macOS:**
```bash
brew install tesseract
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install tesseract-ocr tesseract-ocr-eng tesseract-ocr-fra tesseract-ocr-hin tesseract-ocr-jpn tesseract-ocr-ara tesseract-ocr-chi-sim tesseract-ocr-rus
```

#### 3. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

#### 4. Install Python Dependencies
```bash
pip install -r requirements.txt
```

#### 5. Verify Installation
```bash
python -c "import fitz; import pytesseract; print('Setup successful!')"
```

### Input
- PDF files in the input directory
- Supports any PDF format with text and images

### Output
- JSON files with document title and outline structure
- Each PDF generates a corresponding JSON output file

## Usage

### Local Execution
```bash
python process_pdfs.py
```

### Docker Execution
```bash
# Build the Docker image
docker build --platform linux/amd64 -t pdf-processor .

# Run with sample data
docker run --rm -v $(pwd)/sample_dataset/pdfs:/app/input:ro -v $(pwd)/sample_dataset/outputs:/app/output pdf-processor

# Run with custom input/output directories
docker run --rm -v /path/to/your/pdfs:/app/input:ro -v /path/to/output:/app/output pdf-processor
```

### Docker Commands for Windows
```powershell
# Build the Docker image
docker build --platform linux/amd64 -t pdf-processor .

# Run with sample data (PowerShell)
docker run --rm -v ${PWD}/sample_dataset/pdfs:/app/input:ro -v ${PWD}/sample_dataset/outputs:/app/output pdf-processor

# Run with custom directories
docker run --rm -v C:\path\to\pdfs:/app/input:ro -v C:\path\to\output:/app/output pdf-processor
```

## Performance
- Execution time: ≤ 10 seconds for 50-page PDF
- Model size: ≤ 200MB
- Network: No internet access required
- Runtime: CPU with 8 cores, 16GB RAM

## Repository Information
- **Repository**: https://github.com/DhanviNautiyal/Adobe-Hackathon-Challenge-1a.git
- **Challenge**: Adobe India Hackathon 2025 - Challenge 1a
- **Type**: PDF Processing Solution 