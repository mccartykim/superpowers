#!/usr/bin/env python3
"""
Batch OCR script for folder 008
Processes all JPG files in the specified directory using tesseract
"""

import os
import subprocess
from pathlib import Path

# Define paths
input_dir = Path("/home/user/superpowers/epstein_documents/Epstein Estate Documents - Seventh Production/IMAGES/008/")
output_dir = Path("/home/user/superpowers/epstein_documents/ocr_results/008/")

# Ensure output directory exists
output_dir.mkdir(parents=True, exist_ok=True)

# Get all JPG files
jpg_files = sorted(input_dir.glob("*.jpg"))

print(f"Found {len(jpg_files)} JPG files to process")
print(f"Input directory: {input_dir}")
print(f"Output directory: {output_dir}")
print("-" * 60)

# Process each file
success_count = 0
errors = []

for jpg_file in jpg_files:
    # Create output filename (same base name, .txt extension)
    base_name = jpg_file.stem
    output_file = output_dir / f"{base_name}.txt"

    try:
        # Run tesseract OCR
        # tesseract expects output filename WITHOUT extension
        output_base = str(output_file.with_suffix(''))

        result = subprocess.run(
            ['tesseract', str(jpg_file), output_base],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            success_count += 1
            print(f"✓ Processed: {base_name}.jpg")
        else:
            error_msg = f"{base_name}.jpg - Return code {result.returncode}: {result.stderr}"
            errors.append(error_msg)
            print(f"✗ Failed: {error_msg}")

    except subprocess.TimeoutExpired:
        error_msg = f"{base_name}.jpg - Timeout after 60 seconds"
        errors.append(error_msg)
        print(f"✗ Failed: {error_msg}")
    except Exception as e:
        error_msg = f"{base_name}.jpg - {str(e)}"
        errors.append(error_msg)
        print(f"✗ Failed: {error_msg}")

print("-" * 60)
print(f"\nProcessing complete!")
print(f"Success: {success_count}/{len(jpg_files)}")
print(f"Failures: {len(errors)}")

if errors:
    print("\nErrors:")
    for error in errors:
        print(f"  - {error}")

# Display sample from first successful OCR file
print("\n" + "=" * 60)
print("TEXT SAMPLE (from first file):")
print("=" * 60)

first_output = output_dir / "HOUSE_OVERSIGHT_024477.txt"
if first_output.exists():
    with open(first_output, 'r', encoding='utf-8') as f:
        sample = f.read()[:500]  # First 500 characters
        print(sample)
        if len(sample) == 500:
            print("\n[...truncated...]")
else:
    print("No output file found for sample")
