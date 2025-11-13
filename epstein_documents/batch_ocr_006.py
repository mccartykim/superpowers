#!/usr/bin/env python3
"""
Batch OCR processing for folder 006
Processes HOUSE_OVERSIGHT_020477.jpg through HOUSE_OVERSIGHT_020526.jpg
"""
import os
import subprocess
from pathlib import Path

# Define paths
input_dir = Path("/home/user/superpowers/epstein_documents/Epstein Estate Documents - Seventh Production/IMAGES/006")
output_dir = Path("/home/user/superpowers/epstein_documents/ocr_results/006")

# Create output directory if it doesn't exist
output_dir.mkdir(parents=True, exist_ok=True)

# Track results
success_count = 0
error_count = 0
errors = []

# Process files from HOUSE_OVERSIGHT_020477 to HOUSE_OVERSIGHT_020526
start_num = 20477
end_num = 20526

print(f"Starting OCR processing for {end_num - start_num + 1} files...")
print(f"Input directory: {input_dir}")
print(f"Output directory: {output_dir}")
print("-" * 60)

for num in range(start_num, end_num + 1):
    filename = f"HOUSE_OVERSIGHT_{num:06d}.jpg"
    input_path = input_dir / filename
    output_base = output_dir / f"HOUSE_OVERSIGHT_{num:06d}"
    output_txt = output_dir / f"HOUSE_OVERSIGHT_{num:06d}.txt"

    # Check if input file exists
    if not input_path.exists():
        error_msg = f"Input file not found: {filename}"
        errors.append(error_msg)
        error_count += 1
        print(f"ERROR: {error_msg}")
        continue

    try:
        # Run tesseract OCR
        # tesseract outputs to {output_base}.txt automatically
        result = subprocess.run(
            ["tesseract", str(input_path), str(output_base)],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            success_count += 1
            print(f"[{success_count}/{end_num - start_num + 1}] SUCCESS: {filename}")
        else:
            error_msg = f"{filename}: {result.stderr.strip()}"
            errors.append(error_msg)
            error_count += 1
            print(f"ERROR: {error_msg}")

    except subprocess.TimeoutExpired:
        error_msg = f"{filename}: OCR timeout (>60s)"
        errors.append(error_msg)
        error_count += 1
        print(f"ERROR: {error_msg}")
    except Exception as e:
        error_msg = f"{filename}: {str(e)}"
        errors.append(error_msg)
        error_count += 1
        print(f"ERROR: {error_msg}")

print("-" * 60)
print(f"\nProcessing complete!")
print(f"Successful: {success_count}")
print(f"Errors: {error_count}")

if errors:
    print(f"\nError details:")
    for error in errors:
        print(f"  - {error}")

# Display sample of first successfully processed file
print("\n" + "=" * 60)
print("SAMPLE TEXT FROM FIRST FILE:")
print("=" * 60)
first_output = output_dir / f"HOUSE_OVERSIGHT_{start_num:06d}.txt"
if first_output.exists():
    with open(first_output, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.strip().split('\n')
        # Show first 20 lines or all if less
        sample_lines = lines[:20]
        print('\n'.join(sample_lines))
        if len(lines) > 20:
            print(f"\n... ({len(lines) - 20} more lines)")
else:
    print("No output file found to display sample.")
