#!/usr/bin/env python3
"""
Batch OCR processor for Epstein documents
Processes all JPG and TIF files in the IMAGES directory with parallel processing
"""

import os
import subprocess
import json
from pathlib import Path
from multiprocessing import Pool, cpu_count
from datetime import datetime
import time

# Configuration
IMAGES_DIR = "/home/user/superpowers/epstein_documents/Epstein Estate Documents - Seventh Production/IMAGES"
OUTPUT_DIR = "/home/user/superpowers/epstein_documents/ocr_results"
NUM_WORKERS = min(cpu_count(), 8)  # Use up to 8 cores

# Statistics tracking
stats = {
    "total_files": 0,
    "successful": 0,
    "failed": 0,
    "errors": [],
    "start_time": None,
    "end_time": None,
    "duration_seconds": 0
}

def process_image(image_path):
    """
    Process a single image file with OCR
    Returns tuple: (success, image_path, output_path, error_msg)
    """
    try:
        # Get filename without extension
        filename = Path(image_path).stem

        # Create output path for text file
        output_path = os.path.join(OUTPUT_DIR, f"{filename}.txt")

        # Run tesseract OCR
        result = subprocess.run(
            ['tesseract', image_path, output_path.replace('.txt', ''), '-l', 'eng'],
            capture_output=True,
            text=True,
            timeout=60  # 60 second timeout per image
        )

        if result.returncode == 0:
            # Verify output file was created
            if os.path.exists(output_path):
                return (True, image_path, output_path, None)
            else:
                return (False, image_path, None, "Output file not created")
        else:
            return (False, image_path, None, result.stderr)

    except subprocess.TimeoutExpired:
        return (False, image_path, None, "OCR timeout (>60s)")
    except Exception as e:
        return (False, image_path, None, str(e))

def find_all_images():
    """Find all JPG and TIF files in the IMAGES directory"""
    image_files = []

    for root, dirs, files in os.walk(IMAGES_DIR):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.tif', '.tiff')):
                image_files.append(os.path.join(root, file))

    return sorted(image_files)

def save_results_summary(results):
    """Save a JSON summary of all OCR results"""
    summary = {
        "processing_info": {
            "start_time": stats["start_time"],
            "end_time": stats["end_time"],
            "duration_seconds": stats["duration_seconds"],
            "num_workers": NUM_WORKERS
        },
        "statistics": {
            "total_files": stats["total_files"],
            "successful": stats["successful"],
            "failed": stats["failed"],
            "success_rate": f"{(stats['successful']/stats['total_files']*100):.2f}%" if stats["total_files"] > 0 else "0%"
        },
        "results": [],
        "errors": stats["errors"]
    }

    for success, image_path, output_path, error_msg in results:
        result_entry = {
            "image_file": image_path,
            "success": success
        }

        if success:
            result_entry["ocr_text_file"] = output_path
            # Get file size
            if os.path.exists(output_path):
                result_entry["text_file_size"] = os.path.getsize(output_path)
        else:
            result_entry["error"] = error_msg

        summary["results"].append(result_entry)

    # Save summary JSON
    summary_path = os.path.join(OUTPUT_DIR, "ocr_summary.json")
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)

    print(f"\n✓ Summary saved to: {summary_path}")

def main():
    print("=" * 80)
    print("EPSTEIN DOCUMENTS - BATCH OCR PROCESSOR")
    print("=" * 80)

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Find all images
    print(f"\n[1/4] Scanning for image files in: {IMAGES_DIR}")
    image_files = find_all_images()
    stats["total_files"] = len(image_files)

    print(f"      Found {stats['total_files']} image files")

    if stats["total_files"] == 0:
        print("ERROR: No image files found!")
        return

    # Start processing
    print(f"\n[2/4] Processing images with {NUM_WORKERS} parallel workers")
    print(f"      Output directory: {OUTPUT_DIR}")

    stats["start_time"] = datetime.now().isoformat()
    start_time = time.time()

    # Process images in parallel
    with Pool(processes=NUM_WORKERS) as pool:
        results = []

        # Use imap_unordered for better progress tracking
        for i, result in enumerate(pool.imap_unordered(process_image, image_files), 1):
            results.append(result)
            success, image_path, output_path, error_msg = result

            if success:
                stats["successful"] += 1
                if i % 10 == 0:  # Progress update every 10 files
                    print(f"      Progress: {i}/{stats['total_files']} ({i/stats['total_files']*100:.1f}%) - {stats['successful']} successful")
            else:
                stats["failed"] += 1
                error_entry = {
                    "file": image_path,
                    "error": error_msg
                }
                stats["errors"].append(error_entry)
                print(f"      ✗ FAILED: {Path(image_path).name} - {error_msg}")

    end_time = time.time()
    stats["end_time"] = datetime.now().isoformat()
    stats["duration_seconds"] = round(end_time - start_time, 2)

    # Save results
    print(f"\n[3/4] Saving results and summary")
    save_results_summary(results)

    # Print final statistics
    print(f"\n[4/4] PROCESSING COMPLETE")
    print("=" * 80)
    print(f"STATISTICS:")
    print(f"  Total files:        {stats['total_files']}")
    print(f"  Successfully OCR'd: {stats['successful']} ({stats['successful']/stats['total_files']*100:.1f}%)")
    print(f"  Failed:             {stats['failed']}")
    print(f"  Total time:         {stats['duration_seconds']} seconds")
    print(f"  Average per file:   {stats['duration_seconds']/stats['total_files']:.2f} seconds")
    print(f"\nOUTPUT LOCATION:")
    print(f"  Text files:  {OUTPUT_DIR}/*.txt")
    print(f"  Summary:     {OUTPUT_DIR}/ocr_summary.json")
    print("=" * 80)

    if stats["failed"] > 0:
        print(f"\n⚠ WARNING: {stats['failed']} files failed to process")
        print(f"  See {OUTPUT_DIR}/ocr_summary.json for error details")

if __name__ == "__main__":
    main()
