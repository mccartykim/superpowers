#!/usr/bin/env python3
"""
Batch OCR processing for folder 002
Processes HOUSE_OVERSIGHT_012477.jpg through HOUSE_OVERSIGHT_012526.jpg
"""

import subprocess
import os
from pathlib import Path

# Define paths
source_dir = Path("/home/user/superpowers/epstein_documents/Epstein Estate Documents - Seventh Production/IMAGES/002/")
output_dir = Path("/home/user/superpowers/epstein_documents/ocr_results/002/")

# Ensure output directory exists
output_dir.mkdir(parents=True, exist_ok=True)

# File range
start_num = 12477
end_num = 12526

success_count = 0
errors = []

print(f"Starting OCR processing of {end_num - start_num + 1} files...")
print(f"Source: {source_dir}")
print(f"Output: {output_dir}")
print("-" * 60)

for num in range(start_num, end_num + 1):
    filename = f"HOUSE_OVERSIGHT_{num:06d}.jpg"
    input_path = source_dir / filename
    output_base = output_dir / f"HOUSE_OVERSIGHT_{num:06d}"

    if not input_path.exists():
        error_msg = f"File not found: {filename}"
        errors.append(error_msg)
        print(f"ERROR: {error_msg}")
        continue

    try:
        # Run tesseract (output path without extension, tesseract adds .txt)
        result = subprocess.run(
            ["tesseract", str(input_path), str(output_base)],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            success_count += 1
            print(f"✓ Processed {filename} -> {output_base.name}.txt")
        else:
            error_msg = f"{filename}: {result.stderr.strip()}"
            errors.append(error_msg)
            print(f"✗ Failed {filename}: {result.stderr.strip()}")

    except subprocess.TimeoutExpired:
        error_msg = f"{filename}: Timeout after 60 seconds"
        errors.append(error_msg)
        print(f"✗ {error_msg}")
    except Exception as e:
        error_msg = f"{filename}: {str(e)}"
        errors.append(error_msg)
        print(f"✗ {error_msg}")

print("-" * 60)
print(f"\nProcessing complete!")
print(f"Success: {success_count}/{end_num - start_num + 1}")
print(f"Errors: {len(errors)}")

if errors:
    print("\nError details:")
    for error in errors:
        print(f"  - {error}")

# Show sample from first successful file
if success_count > 0:
    print("\n" + "=" * 60)
    print("SAMPLE OUTPUT (first 500 characters from first file):")
    print("=" * 60)
    first_output = output_dir / f"HOUSE_OVERSIGHT_{start_num:06d}.txt"
    if first_output.exists():
        with open(first_output, 'r', encoding='utf-8') as f:
            sample = f.read(500)
            print(sample)
            if len(sample) == 500:
                print("\n[...truncated...]")
