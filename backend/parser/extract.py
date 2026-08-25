import json
import os
from pathlib import Path
from pdf_reader import open_pdf, get_page_text, get_page_image
from ocr import ocr_image

RAW = Path(r"backend\knowledge_base\raw")
OUTPUT = Path(r"backend\knowledge_base\extracted")


def extract_pdf(pdf_path):
    """Extract text from every page, falling back to OCR for scanned pages."""
    doc = open_pdf(pdf_path)
    pages = []
    for i, page in enumerate(doc):
        text = get_page_text(page)
        used_ocr = False
        if len(text.split()) < 30:
            img = get_page_image(page)
            text = ocr_image(img)
            used_ocr = True
        pages.append({
            "page": i + 1,
            "text": text,
            "ocr_used": used_ocr
        })
    doc.close()
    return pages

def save_extracted(pdf_path, pages, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.splitext(os.path.basename(str(pdf_path)))[0] + ".json"
    output_path = os.path.join(str(output_dir), filename)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({"source": str(pdf_path), "pages": pages}, f, ensure_ascii=False, indent=2)
    return output_path

def run_batch():
    pdf_files = list(RAW.rglob("*.pdf"))
    print(f"Found {len(pdf_files)} PDF(s) under {RAW}\n")

    ocr_count = 0
    fail_count = 0

    for pdf in pdf_files:
        relative_folder = pdf.parent.relative_to(RAW)
        output_dir = OUTPUT / relative_folder

        print(f"Processing: {pdf}")
        try:
            data = extract_pdf(pdf)
            saved_path = save_extracted(pdf, data, output_dir)

            pages_with_ocr = sum(1 for p in data if p["ocr_used"])
            if pages_with_ocr:
                ocr_count += 1
                print(f"  -> saved to {saved_path} ({pages_with_ocr}/{len(data)} pages used OCR)")
            else:
                print(f"  -> saved to {saved_path}")

        except Exception as e:
            fail_count += 1
            print(f"  !! FAILED: {e}")

    print("\n--- Summary ---")
    print(f"Total files: {len(pdf_files)}")
    print(f"Files needing OCR: {ocr_count}")
    print(f"Failed: {fail_count}")

if __name__ == "__main__":
    run_batch()