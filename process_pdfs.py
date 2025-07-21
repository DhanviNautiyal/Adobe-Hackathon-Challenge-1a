import os
import json
from pathlib import Path
import fitz

def process_pdfs():
    # Get input and output directories
    input_dir = Path("/app/input")
    output_dir = Path("/app/output")
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Get all PDF files
    pdf_files = list(input_dir.glob("*.pdf"))
    
    for pdf_file in pdf_files:
        # Create dummy JSON data
        dummy_data = {
            "title": "Understanding AI",
            "outline": [
                {
                    "level": "H1",
                    "text": "Introduction",
                    "page": 1
                },
                {
                    "level": "H2",
                    "text": "What is AI?",
                    "page": 2
                },
                {
                    "level": "H3",
                    "text": "History of AI",
                    "page": 3
                }
            ]
        }
        
        # Create output JSON file
        output_file = output_dir / f"{pdf_file.stem}.json"
        with open(output_file, "w") as f:
            json.dump(dummy_data, f, indent=2)
        
        print(f"Processed {pdf_file.name} -> {output_file.name}")

def extract_pdf_content(pdf_path):
    """
    Extracts text blocks with font size, bold status, and position using PyMuPDF.
    """
    doc = fitz.open(pdf_path)
    blocks = []
    for page_num, page in enumerate(doc, start=1):
        text_dict = page.get_text("dict")
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
    return blocks

if __name__ == "__main__":
    print("Starting processing pdfs")
    process_pdfs() 
    print("completed processing pdfs")

    # Basic test for extract_pdf_content
    sample_pdf = Path(__file__).parent / "sample_dataset" / "pdfs" / "file01.pdf"
    print(f"Extracting text blocks from {sample_pdf}")
    extracted_blocks = extract_pdf_content(sample_pdf)
    for block in extracted_blocks[:5]:
        print(block)
    print(f"Extracted total {len(extracted_blocks)} blocks from {sample_pdf}")