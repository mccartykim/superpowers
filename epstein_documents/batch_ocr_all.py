#!/usr/bin/env python3
"""
Batch OCR script for Epstein Estate Documents
Processes all .jpg and .tif files in the IMAGES directory
"""

import os
import sys
from pathlib import Path
from PIL import Image
import pytesseract

# Configuration
IMAGES_DIR = "/home/user/superpowers/epstein_documents/Epstein Estate Documents - Seventh Production/IMAGES/"
OUTPUT_DIR = "/home/user/superpowers/epstein_documents/ocr_results/"

def setup_output_directory():
    """Create output directory structure"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Output directory: {OUTPUT_DIR}")

def find_image_files():
    """Find all .jpg and .tif files recursively"""
    image_files = []
    for root, dirs, files in os.walk(IMAGES_DIR):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.tif', '.tiff')):
                image_files.append(os.path.join(root, file))
    return sorted(image_files)

def get_output_path(image_path):
    """Generate output path maintaining folder structure"""
    # Get relative path from IMAGES_DIR
    rel_path = os.path.relpath(image_path, IMAGES_DIR)
    # Change extension to .txt
    txt_filename = os.path.splitext(rel_path)[0] + '.txt'
    # Create full output path
    output_path = os.path.join(OUTPUT_DIR, txt_filename)
    # Create subdirectory if needed
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    return output_path

def ocr_image(image_path):
    """Perform OCR on a single image"""
    try:
        # Open image
        image = Image.open(image_path)
        # Perform OCR
        text = pytesseract.image_to_string(image)
        return text, None
    except Exception as e:
        return None, str(e)

def main():
    print("=" * 80)
    print("Epstein Estate Documents - Batch OCR")
    print("=" * 80)

    # Setup
    setup_output_directory()

    # Find all images
    print("\nSearching for image files...")
    image_files = find_image_files()
    total_files = len(image_files)
    print(f"Found {total_files} image files to process")

    # Statistics
    success_count = 0
    error_count = 0
    error_log = []

    # Process each image
    print("\nStarting OCR processing...")
    print("-" * 80)

    for idx, image_path in enumerate(image_files, 1):
        filename = os.path.basename(image_path)
        folder = os.path.basename(os.path.dirname(image_path))

        # Perform OCR
        text, error = ocr_image(image_path)

        if error is None:
            # Save to output file
            output_path = get_output_path(image_path)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text)
            success_count += 1

            # Progress tracking (every 10 files)
            if idx % 10 == 0:
                print(f"Progress: {idx}/{total_files} files processed ({success_count} successful, {error_count} errors)")
        else:
            # Log error
            error_count += 1
            error_msg = f"{folder}/{filename}: {error}"
            error_log.append(error_msg)
            print(f"ERROR [{idx}/{total_files}] {error_msg}")

    # Final summary
    print("\n" + "=" * 80)
    print("OCR Processing Complete")
    print("=" * 80)
    print(f"Total files processed: {total_files}")
    print(f"Successfully OCRed: {success_count}")
    print(f"Errors encountered: {error_count}")
    print(f"Output directory: {OUTPUT_DIR}")

    if error_log:
        print("\n" + "-" * 80)
        print("Error Summary:")
        print("-" * 80)
        for error_msg in error_log:
            print(f"  - {error_msg}")

    # Save error log if there were errors
    if error_log:
        error_log_path = os.path.join(OUTPUT_DIR, "error_log.txt")
        with open(error_log_path, 'w') as f:
            f.write("OCR Error Log\n")
            f.write("=" * 80 + "\n\n")
            for error_msg in error_log:
                f.write(error_msg + "\n")
        print(f"\nError log saved to: {error_log_path}")

    print("\n" + "=" * 80)
    return 0 if error_count == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
