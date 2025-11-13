#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path

# Define paths
input_dir = "/home/user/superpowers/epstein_documents/Epstein Estate Documents - Seventh Production/IMAGES/005/"
output_dir = "/home/user/superpowers/epstein_documents/ocr_results/005/"

# Initialize counters
success_count = 0
error_count = 0
errors = []
samples = []

# Get all JPG files
jpg_files = sorted([f for f in os.listdir(input_dir) if f.endswith('.jpg')])

print(f"Found {len(jpg_files)} JPG files to process")
print("Starting OCR processing...\n")

for i, jpg_file in enumerate(jpg_files, 1):
    input_path = os.path.join(input_dir, jpg_file)
    base_name = os.path.splitext(jpg_file)[0]
    output_path = os.path.join(output_dir, base_name)

    try:
        # Run tesseract OCR (tesseract adds .txt extension automatically)
        result = subprocess.run(
            ['tesseract', input_path, output_path],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            success_count += 1
            print(f"[{i}/{len(jpg_files)}] ✓ {jpg_file}")

            # Collect sample from first 3 successful OCRs
            if len(samples) < 3:
                txt_file = output_path + '.txt'
                if os.path.exists(txt_file):
                    with open(txt_file, 'r', encoding='utf-8') as f:
                        content = f.read().strip()
                        if content:
                            samples.append({
                                'file': jpg_file,
                                'text': content[:300]  # First 300 chars
                            })
        else:
            error_count += 1
            error_msg = f"{jpg_file}: {result.stderr}"
            errors.append(error_msg)
            print(f"[{i}/{len(jpg_files)}] ✗ {jpg_file} - {result.stderr}")

    except subprocess.TimeoutExpired:
        error_count += 1
        error_msg = f"{jpg_file}: Timeout (>60s)"
        errors.append(error_msg)
        print(f"[{i}/{len(jpg_files)}] ✗ {jpg_file} - Timeout")

    except Exception as e:
        error_count += 1
        error_msg = f"{jpg_file}: {str(e)}"
        errors.append(error_msg)
        print(f"[{i}/{len(jpg_files)}] ✗ {jpg_file} - {str(e)}")

# Print summary
print("\n" + "="*70)
print("OCR PROCESSING COMPLETE")
print("="*70)
print(f"Total files: {len(jpg_files)}")
print(f"Successful: {success_count}")
print(f"Failed: {error_count}")
print()

if errors:
    print("ERRORS:")
    for error in errors:
        print(f"  - {error}")
    print()

if samples:
    print("TEXT SAMPLES:")
    print("-"*70)
    for sample in samples:
        print(f"\nFile: {sample['file']}")
        print(f"Preview: {sample['text'][:200]}...")
        print("-"*70)
