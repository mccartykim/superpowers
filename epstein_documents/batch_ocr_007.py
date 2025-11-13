#!/usr/bin/env python3
import subprocess
import os
from pathlib import Path

# Define paths
input_dir = "/home/user/superpowers/epstein_documents/Epstein Estate Documents - Seventh Production/IMAGES/007/"
output_dir = "/home/user/superpowers/epstein_documents/ocr_results/007/"

# Get all JPG files
jpg_files = sorted([f for f in os.listdir(input_dir) if f.endswith('.jpg')])

print(f"Found {len(jpg_files)} JPG files to process")
print(f"Input directory: {input_dir}")
print(f"Output directory: {output_dir}")
print("-" * 80)

success_count = 0
error_count = 0
errors = []

for i, jpg_file in enumerate(jpg_files, 1):
    input_path = os.path.join(input_dir, jpg_file)
    base_name = os.path.splitext(jpg_file)[0]
    output_path = os.path.join(output_dir, base_name)

    print(f"[{i}/{len(jpg_files)}] Processing: {jpg_file}...", end=" ")

    try:
        # Run tesseract OCR
        result = subprocess.run(
            ['tesseract', input_path, output_path],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            print("SUCCESS")
            success_count += 1
        else:
            print(f"FAILED (return code: {result.returncode})")
            error_count += 1
            errors.append(f"{jpg_file}: {result.stderr}")
    except subprocess.TimeoutExpired:
        print("TIMEOUT")
        error_count += 1
        errors.append(f"{jpg_file}: Timeout after 60 seconds")
    except Exception as e:
        print(f"ERROR: {str(e)}")
        error_count += 1
        errors.append(f"{jpg_file}: {str(e)}")

print("-" * 80)
print(f"\nProcessing complete!")
print(f"Success: {success_count}")
print(f"Errors: {error_count}")

if errors:
    print("\nErrors encountered:")
    for error in errors:
        print(f"  - {error}")

# Show sample output from first successful file
print("\n" + "=" * 80)
print("SAMPLE OUTPUT (from first file):")
print("=" * 80)
first_txt = os.path.join(output_dir, "HOUSE_OVERSIGHT_022477.txt")
if os.path.exists(first_txt):
    with open(first_txt, 'r', encoding='utf-8') as f:
        content = f.read()
        print(content[:500] if len(content) > 500 else content)
        if len(content) > 500:
            print("\n... (truncated)")
else:
    print("Sample file not found")
