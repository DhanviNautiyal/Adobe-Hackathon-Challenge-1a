import os
import json
from pathlib import Path
import fitz
import pytesseract
from PIL import Image
from pytesseract import Output

def process_pdfs():
    # Determine input and output directories (container vs local)
    script_dir = Path(__file__).parent
    container_input = Path("/app/input")
    container_output = Path("/app/output")
    # Use container paths if they exist and have PDFs, otherwise fallback to local sample_dataset
    if container_input.exists() and any(container_input.glob("*.pdf")):
        input_dir = container_input
    else:
        input_dir = script_dir / "sample_dataset" / "pdfs"
    if container_output.exists():
        output_dir = container_output
    else:
        output_dir = script_dir / "sample_dataset" / "outputs"
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    # Get all PDF files
    pdf_files = list(input_dir.glob("*.pdf"))
    
    for pdf_file in pdf_files:
        # Extract text blocks including OCR from images
        blocks = extract_pdf_content(pdf_file)

        # Create output JSON file
        output_file = output_dir / f"{pdf_file.stem}.json"
        # Write JSON with UTF-8 encoding and preserve unicode characters
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump({"blocks": blocks}, f, ensure_ascii=False, indent=2)
    
        print(f"Processed {pdf_file.name} -> {output_file.name}")

def extract_pdf_content(pdf_path):
    """
    Extracts text blocks with font size, bold status, and position using PyMuPDF (multilingual).
    """
    doc = fitz.open(pdf_path)
    blocks = []
    for page_num, page in enumerate(doc, start=1):
        # Use rawdict to preserve unicode text ordering and support multilingual PDFs
        text_dict = page.get_text("rawdict")
        for b in text_dict["blocks"]:
            if b.get("type") != 0:
                continue
            for line in b.get("lines", []):
                for span in line.get("spans", []):
                    x0, y0, x1, y1 = span.get("bbox", [0,0,0,0])
                    blocks.append({
                        "text": span.get("text", ""),
                        "page": page_num,
                        "font_size": span.get("size"),
                        "font_name": span.get("font", ""),
                        "is_bold": "Bold" in span.get("font", ""),
                        "x0": x0,
                        "y0": y0
                    })
        # OCR image-based text extraction
        for img in page.get_images(full=True):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            if pix.n < 5:
                img_pil = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            else:
                pix0 = fitz.Pixmap(fitz.csRGB, pix)
                img_pil = Image.frombytes("RGB", [pix0.width, pix0.height], pix0.samples)
            ocr_data = pytesseract.image_to_data(img_pil, output_type=Output.DICT)
            for i, text in enumerate(ocr_data["text"]):
                text = text.strip()
                if not text:
                    continue
                blocks.append({
                    "text": text,
                    "page": page_num,
                    "font_size": ocr_data["height"][i],
                    "font_name": None,
                    "is_bold": False,
                    "x0": ocr_data["left"][i],
                    "y0": ocr_data["top"][i]
                })
    return blocks

if __name__ == "__main__":
    print("Starting processing pdfs")
    process_pdfs()
    print("completed processing pdfs")

    # Basic test for multilingual extract_pdf_content
    sample_pdf = Path(__file__).parent / "sample_dataset" / "pdfs" / "file01.pdf"
    print(f"Extracting text blocks from {sample_pdf}")
    extracted_blocks = extract_pdf_content(sample_pdf)
    for block in extracted_blocks[:5]:
        # Print JSON-formatted block to preserve unicode
        print(json.dumps(block, ensure_ascii=False))
    print(f"Extracted total {len(extracted_blocks)} blocks from {sample_pdf}")