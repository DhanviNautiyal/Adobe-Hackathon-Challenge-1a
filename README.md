# Challenge 1a: PDF Processing Solution

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

## Input
- PDF files in the input directory
- Supports any PDF format with text and images

## Output
- JSON files with document title and outline structure
- Each PDF generates a corresponding JSON output file

## Usage
```bash
python process_pdfs.py
```

## Performance
- Execution time: ≤ 10 seconds for 50-page PDF
- Model size: ≤ 200MB
- Network: No internet access required
- Runtime: CPU with 8 cores, 16GB RAM 