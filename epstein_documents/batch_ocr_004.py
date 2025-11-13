#!/usr/bin/env python3
"""
Batch OCR script for folder 004
Processes all JPG and TIF files in the folder using tesseract
"""

import os
import subprocess
from pathlib import Path

# Paths
input_dir = "/home/user/superpowers/epstein_documents/Epstein Estate Documents - Seventh Production/IMAGES/004/"
output_dir = "/home/user/superpowers/epstein_documents/ocr_results/004/"

# Stats tracking
success_count = 0
error_count = 0
errors = []

# Get all image files (jpg and tif)
image_files = []
for ext in ['*.jpg', '*.JPG', '*.tif', '*.tiff', '*.TIF', '*.TIFF']:
    image_files.extend(Path(input_dir).glob(ext))

# Sort by filename
image_files.sort()

print(f"Found {len(image_files)} image files to process")
print(f"Output directory: {output_dir}\n")

# Process each file
for img_file in image_files:
    basename = img_file.stem
    output_file = os.path.join(output_dir, f"{basename}.txt")

    try:
        print(f"Processing: {img_file.name}...", end=" ")

        # Run tesseract OCR
        # tesseract expects output filename without extension
        output_base = os.path.join(output_dir, basename)
        result = subprocess.run(
            ['tesseract', str(img_file), output_base],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            success_count += 1
            print("✓ Success")
        else:
            error_count += 1
            error_msg = f"{img_file.name}: {result.stderr.strip()}"
            errors.append(error_msg)
            print(f"✗ Failed: {result.stderr.strip()}")

    except subprocess.TimeoutExpired:
        error_count += 1
        error_msg = f"{img_file.name}: Timeout (>60s)"
        errors.append(error_msg)
        print(f"✗ Failed: Timeout")
    except Exception as e:
        error_count += 1
        error_msg = f"{img_file.name}: {str(e)}"
        errors.append(error_msg)
        print(f"✗ Failed: {str(e)}")

# Summary
print("\n" + "="*60)
print("BATCH OCR COMPLETE")
print("="*60)
print(f"Total files processed: {len(image_files)}")
print(f"Successful: {success_count}")
print(f"Failed: {error_count}")

if errors:
    print("\nErrors encountered:")
    for error in errors:
        print(f"  - {error}")

# Show sample from first successfully processed file
print("\n" + "="*60)
print("SAMPLE TEXT FROM FIRST FILE")
print("="*60)
txt_files = sorted(Path(output_dir).glob("*.txt"))
if txt_files:
    sample_file = txt_files[0]
    print(f"File: {sample_file.name}")
    print("-"*60)
    with open(sample_file, 'r', encoding='utf-8') as f:
        content = f.read()
        # Show first 500 characters
        preview = content[:500]
        print(preview)
        if len(content) > 500:
            print(f"\n... (showing first 500 of {len(content)} characters)")
else:
    print("No output files found")
