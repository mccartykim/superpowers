#!/usr/bin/env python3
"""
Batch OCR script for Epstein Estate Documents - Folder 001
OCRs all JPG files in folder 001 and saves results as text files
"""

import os
import sys
from pathlib import Path
from PIL import Image
import pytesseract
from datetime import datetime

# Configuration
INPUT_DIR = "epstein_documents/Epstein Estate Documents - Seventh Production/IMAGES/001/"
OUTPUT_DIR = "epstein_documents/ocr_results/001/"
SUMMARY_FILE = "epstein_documents/ocr_results/001/ocr_summary.txt"

def ensure_output_dir():
    """Create output directory if it doesn't exist"""
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {OUTPUT_DIR}")

def get_jpg_files():
    """Get all JPG files from input directory"""
    input_path = Path(INPUT_DIR)
    jpg_files = sorted(input_path.glob("*.jpg"))
    print(f"Found {len(jpg_files)} JPG files")
    return jpg_files

def ocr_image(image_path):
    """
    OCR a single image file
    Returns: (success, text, error_message)
    """
    try:
        # Open and OCR the image
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang='eng')
        return (True, text, None)
    except Exception as e:
        return (False, None, str(e))

def save_ocr_result(output_path, text):
    """Save OCR text to file"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)

def batch_ocr():
    """Main batch OCR function"""
    print("=" * 70)
    print("Batch OCR - Epstein Estate Documents - Folder 001")
    print("=" * 70)
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Setup
    ensure_output_dir()
    jpg_files = get_jpg_files()

    if not jpg_files:
        print("ERROR: No JPG files found!")
        return

    # Process files
    successful = []
    failed = []

    for idx, jpg_file in enumerate(jpg_files, 1):
        filename = jpg_file.name
        print(f"[{idx}/{len(jpg_files)}] Processing: {filename}...", end=" ", flush=True)

        # OCR the image
        success, text, error = ocr_image(jpg_file)

        if success:
            # Save result
            output_filename = jpg_file.stem + ".txt"
            output_path = Path(OUTPUT_DIR) / output_filename
            save_ocr_result(output_path, text)
            successful.append(filename)
            print(f"✓ ({len(text)} chars)")
        else:
            failed.append((filename, error))
            print(f"✗ ERROR: {error}")

    # Generate summary
    print("\n" + "=" * 70)
    print("OCR SUMMARY")
    print("=" * 70)
    print(f"Total files: {len(jpg_files)}")
    print(f"Successful: {len(successful)}")
    print(f"Failed: {len(failed)}")
    print(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Write summary file
    with open(SUMMARY_FILE, 'w', encoding='utf-8') as f:
        f.write("OCR Summary - Folder 001\n")
        f.write("=" * 70 + "\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"Total files processed: {len(jpg_files)}\n")
        f.write(f"Successful: {len(successful)}\n")
        f.write(f"Failed: {len(failed)}\n\n")

        if failed:
            f.write("FAILED FILES:\n")
            f.write("-" * 70 + "\n")
            for filename, error in failed:
                f.write(f"{filename}: {error}\n")
        else:
            f.write("All files processed successfully!\n")

    print(f"\nSummary saved to: {SUMMARY_FILE}")

    # Show sample text from first 3 successful files
    if successful:
        print("\n" + "=" * 70)
        print("SAMPLE OCR TEXT (first 3 files)")
        print("=" * 70)
        for filename in successful[:3]:
            txt_filename = Path(filename).stem + ".txt"
            txt_path = Path(OUTPUT_DIR) / txt_filename
            with open(txt_path, 'r', encoding='utf-8') as f:
                text = f.read()
            print(f"\n--- {filename} ---")
            # Show first 300 characters
            preview = text[:300].strip()
            if len(text) > 300:
                preview += "..."
            print(preview)
            print()

if __name__ == "__main__":
    try:
        batch_ocr()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nFATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
