import os
import json
import time
from pathlib import Path
from collections import defaultdict
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import shared_pdf_utils as pdf_utils

MAX_PAGES_FOR_OUTLINE = 25
MAX_IMAGES_PER_DOC = 10

def extract_outline_from_blocks(blocks):
    if not blocks:
        return "Untitled Document", []
        
    sorted_blocks = sorted(blocks, key=lambda b: (b["page"], b["y0"]))
    
    font_sizes = [block["font_size"] for block in sorted_blocks if block["font_size"]]
    font_counts = defaultdict(int)
    for size in font_sizes:
        font_counts[round(size, 1)] += 1
    
    if not font_counts:
        return "Untitled Document", []
        
    body_font_size = max(font_counts.items(), key=lambda x: x[1])[0]
    
    heading_sizes = sorted([size for size in font_counts.keys() 
                           if size > body_font_size and font_counts[size] < font_counts[body_font_size] * 0.5],
                          reverse=True)
    
    size_to_level = {}
    for i, size in enumerate(heading_sizes[:6]):
        size_to_level[size] = f"H{i+1}"
    
    outline = []
    title = None
    
    for block in sorted_blocks[:50]:
        size = round(block["font_size"], 1) if block["font_size"] else 0
        is_bold = block["is_bold"]
        text = block["text"].strip()
        
        if not text:
            continue
            
        if not title and size > body_font_size and is_bold and len(text) < 100:
            title = text
            continue
            
        if size in size_to_level:
            outline.append({
                "level": size_to_level[size],
                "text": text,
                "page": block["page"]
            })
        elif is_bold and size >= body_font_size and len(text) < 100:
            outline.append({
                "level": "H6",
                "text": text,
                "page": block["page"]
            })
        
        if len(outline) >= 15:
            break
    
    return title or "Untitled Document", outline[:10]

def process_single_pdf(pdf_file, output_dir):
    file_start_time = time.time()
    
    try:
        print(f"Starting to process {pdf_file.name}...")
        
        blocks = pdf_utils.extract_pdf_content(pdf_file, MAX_PAGES_FOR_OUTLINE, MAX_IMAGES_PER_DOC)
        
        print(f"Extracted {len(blocks)} blocks from {pdf_file.name}")
        
        title, outline = extract_outline_from_blocks(blocks)
        
        print(f"Extracted title: '{title}' and {len(outline)} outline items from {pdf_file.name}")
        
        output_data = {
            "title": title,
            "outline": outline
        }
        
        output_file = output_dir / f"{pdf_file.stem}.json"
        
        print(f"Creating output file: {output_file}")
        
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        print(f"Successfully created {output_file}")
        
        file_processing_time = time.time() - file_start_time
        return file_processing_time
        
    except Exception as e:
        print(f"Error processing {pdf_file.name}: {str(e)}")
        import traceback
        traceback.print_exc()
        return time.time() - file_start_time

def process_pdfs():
    start_time = time.time()
    
    script_dir = Path(__file__).parent
    container_input = Path("/app/input")
    container_output = Path("/app/output")
    
    if container_input.exists() and any(container_input.glob("*.pdf")) and os.name != 'nt':
        input_dir = container_input
    else:
        input_dir = script_dir / "sample_dataset" / "pdfs"
        
    if container_output.exists() and os.name != 'nt':
        output_dir = container_output
    else:
        output_dir = script_dir / "sample_dataset" / "outputs"
        
    print(f"Using input directory: {input_dir}")
    print(f"Using output directory: {output_dir}")
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    pdf_files = list(input_dir.glob("*.pdf"))
    
    print(f"Found {len(pdf_files)} PDF files to process")
    
    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(pdf_utils.MAX_CORES, len(pdf_files))) as executor:
        futures = {executor.submit(process_single_pdf, pdf_file, output_dir): pdf_file for pdf_file in pdf_files}
        
        for future in concurrent.futures.as_completed(futures):
            pdf_file = futures[future]
            try:
                file_processing_time = future.result()
                print(f"Processed {pdf_file.name} in {file_processing_time:.2f} seconds")
            except Exception as e:
                print(f"Error processing {pdf_file.name}: {str(e)}")
    
    total_time = time.time() - start_time
    print(f"Total processing time: {total_time:.2f} seconds")

if __name__ == "__main__":
    print("Starting PDF processing...")
    process_pdfs()
    print("Completed PDF processing")