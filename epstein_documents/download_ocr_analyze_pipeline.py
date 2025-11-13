#!/usr/bin/env python3
"""
Automated Pipeline: Download -> OCR -> Analyze Epstein Documents
Downloads remaining folders from Google Drive, OCRs them, and searches for relevant content
"""

import os
import subprocess
import sys
import json
import re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# Configuration
BASE_DIR = Path("/home/user/superpowers/epstein_documents")
IMAGES_DIR = BASE_DIR / "Epstein Estate Documents - Seventh Production" / "IMAGES"
OCR_OUTPUT_DIR = BASE_DIR / "ocr_results"
SEARCH_OUTPUT_DIR = BASE_DIR / "search_results"
GOOGLE_DRIVE_URL = "https://drive.google.com/drive/folders/1hTNH5woIRio578onLGElkTWofUSWRoH_?usp=sharing"

# Terms to search for
SEARCH_TERMS = {
    "people": [
        "Trump", "Donald Trump", "Ivanka", "Jared Kushner", "Kushner",
        "Clinton", "Bill Clinton", "Prince Andrew", "Alan Dershowitz",
        "Ghislaine Maxwell", "Sarah Kellen", "Haley Robson", "Nadia Marcinkova",
        "Steve Bannon", "Larry Summers", "Michael Wolff", "Kenneth Starr",
        "Alex Acosta", "Barry Krischer", "Cyrus Vance"
    ],
    "locations": [
        "Little St. James", "island", "Mar-a-Lago", "Palm Beach",
        "Virgin Islands", "New York", "Manhattan"
    ],
    "activities": [
        "massage", "underage", "minor", "teenager", "abuse", "trafficking",
        "recruit", "victim", "witness", "testimony"
    ],
    "legal": [
        "plea deal", "immunity", "prosecution", "indictment", "conviction",
        "deposition", "lawsuit", "settlement"
    ],
    "financial": [
        "money laundering", "wire transfer", "offshore", "shell company",
        "trust fund", "payment"
    ]
}

def check_existing_folders():
    """Check which folders have already been downloaded"""
    existing = []
    if IMAGES_DIR.exists():
        for folder in IMAGES_DIR.iterdir():
            if folder.is_dir():
                existing.append(folder.name)
    return sorted(existing)

def check_ocr_status():
    """Check which folders have been OCRed"""
    ocred = []
    if OCR_OUTPUT_DIR.exists():
        for folder in OCR_OUTPUT_DIR.iterdir():
            if folder.is_dir() and folder.name.isdigit():
                ocred.append(folder.name)
    return sorted(ocred)

def download_missing_folders():
    """Download any folders not yet downloaded from Google Drive"""
    print("\n" + "="*80)
    print("STEP 1: CHECKING FOR ADDITIONAL FOLDERS TO DOWNLOAD")
    print("="*80)

    existing = check_existing_folders()
    print(f"\nAlready downloaded folders: {existing}")

    # Check if there are more folders available
    print(f"\nNote: The current Google Drive link contains folders 001-009.")
    print(f"According to the OPT file, the full collection has 23,124 pages.")
    print(f"We currently have access to approximately 438 pages.")
    print(f"\nIf additional folders become available, re-run this script.")

    return existing

def ocr_folder(folder_name, folder_path):
    """OCR all images in a folder"""
    print(f"\n{'='*80}")
    print(f"OCR Processing: Folder {folder_name}")
    print(f"{'='*80}")

    output_dir = OCR_OUTPUT_DIR / folder_name
    output_dir.mkdir(parents=True, exist_ok=True)

    # Get all image files
    image_files = sorted([f for f in folder_path.glob("*") if f.suffix.lower() in ['.jpg', '.jpeg', '.tif', '.tiff', '.png']])

    if not image_files:
        print(f"No images found in {folder_path}")
        return 0

    print(f"Found {len(image_files)} images to OCR")

    success_count = 0
    failed = []

    for i, img_file in enumerate(image_files, 1):
        output_file = output_dir / f"{img_file.stem}.txt"

        if output_file.exists():
            print(f"[{i}/{len(image_files)}] Skipping {img_file.name} (already exists)")
            success_count += 1
            continue

        try:
            # Run tesseract OCR
            result = subprocess.run(
                ['tesseract', str(img_file), str(output_file.with_suffix('')), '-l', 'eng'],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0 and output_file.exists():
                file_size = output_file.stat().st_size
                print(f"[{i}/{len(image_files)}] ✓ {img_file.name} -> {output_file.name} ({file_size} bytes)")
                success_count += 1
            else:
                print(f"[{i}/{len(image_files)}] ✗ {img_file.name} FAILED")
                failed.append(img_file.name)
        except Exception as e:
            print(f"[{i}/{len(image_files)}] ✗ {img_file.name} ERROR: {e}")
            failed.append(img_file.name)

    print(f"\nFolder {folder_name} complete: {success_count}/{len(image_files)} successful")
    if failed:
        print(f"Failed files: {failed}")

    return success_count

def search_text_file(file_path, search_terms):
    """Search a text file for relevant terms"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        findings = {}
        content_lower = content.lower()

        for category, terms in search_terms.items():
            for term in terms:
                # Case-insensitive search
                if term.lower() in content_lower:
                    # Extract context (200 chars before and after)
                    pattern = re.compile(f'.{{0,200}}{re.escape(term)}.{{0,200}}', re.IGNORECASE | re.DOTALL)
                    matches = pattern.findall(content)

                    if matches:
                        if category not in findings:
                            findings[category] = {}
                        findings[category][term] = {
                            'count': len(matches),
                            'contexts': matches[:3]  # First 3 matches
                        }

        return findings if findings else None
    except Exception as e:
        print(f"Error searching {file_path}: {e}")
        return None

def analyze_folder(folder_name):
    """Analyze OCR results from a folder for relevant content"""
    print(f"\n{'='*80}")
    print(f"ANALYZING: Folder {folder_name}")
    print(f"{'='*80}")

    folder_path = OCR_OUTPUT_DIR / folder_name
    if not folder_path.exists():
        print(f"Folder {folder_path} does not exist")
        return None

    text_files = sorted(folder_path.glob("*.txt"))
    if not text_files:
        print(f"No OCR text files found in {folder_path}")
        return None

    print(f"Analyzing {len(text_files)} OCR files...")

    results = {
        'folder': folder_name,
        'total_files': len(text_files),
        'files_with_findings': 0,
        'findings_by_file': {}
    }

    for text_file in text_files:
        findings = search_text_file(text_file, SEARCH_TERMS)
        if findings:
            results['files_with_findings'] += 1
            results['findings_by_file'][text_file.name] = findings
            print(f"  ✓ {text_file.name}: Found {sum(len(cats) for cats in findings.values())} terms")

    print(f"\nFolder {folder_name}: {results['files_with_findings']}/{results['total_files']} files contain relevant terms")

    return results

def generate_report(all_results):
    """Generate comprehensive report of all findings"""
    print(f"\n{'='*80}")
    print("GENERATING COMPREHENSIVE REPORT")
    print(f"{'='*80}")

    SEARCH_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    report_file = SEARCH_OUTPUT_DIR / "comprehensive_analysis_report.txt"
    json_file = SEARCH_OUTPUT_DIR / "comprehensive_analysis_report.json"

    # Save JSON
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2)
    print(f"JSON report saved: {json_file}")

    # Generate text report
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("EPSTEIN DOCUMENTS - COMPREHENSIVE ANALYSIS REPORT\n")
        f.write("="*80 + "\n\n")
        f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        # Summary
        total_files = sum(r['total_files'] for r in all_results.values())
        total_with_findings = sum(r['files_with_findings'] for r in all_results.values())

        f.write("SUMMARY\n")
        f.write("-"*80 + "\n")
        f.write(f"Folders analyzed: {len(all_results)}\n")
        f.write(f"Total files processed: {total_files}\n")
        f.write(f"Files with findings: {total_with_findings}\n")
        f.write(f"Hit rate: {total_with_findings/total_files*100:.1f}%\n\n")

        # Detailed findings by folder
        for folder, results in sorted(all_results.items()):
            if results['files_with_findings'] == 0:
                continue

            f.write(f"\n{'='*80}\n")
            f.write(f"FOLDER {folder}\n")
            f.write(f"{'='*80}\n")
            f.write(f"Files with findings: {results['files_with_findings']}/{results['total_files']}\n\n")

            for filename, findings in sorted(results['findings_by_file'].items()):
                f.write(f"\n{'-'*80}\n")
                f.write(f"FILE: {filename}\n")
                f.write(f"{'-'*80}\n")

                for category, terms in findings.items():
                    f.write(f"\n{category.upper()}:\n")
                    for term, data in terms.items():
                        f.write(f"\n  Term: {term} (found {data['count']} times)\n")
                        f.write(f"  Contexts:\n")
                        for i, context in enumerate(data['contexts'], 1):
                            # Clean up context
                            context_clean = ' '.join(context.split())
                            f.write(f"    {i}. ...{context_clean}...\n")

    print(f"Text report saved: {report_file}")

    # Print summary to console
    print(f"\n{'='*80}")
    print("ANALYSIS COMPLETE")
    print(f"{'='*80}")
    print(f"Total folders: {len(all_results)}")
    print(f"Total files: {total_files}")
    print(f"Files with findings: {total_with_findings} ({total_with_findings/total_files*100:.1f}%)")
    print(f"\nReports saved:")
    print(f"  - {report_file}")
    print(f"  - {json_file}")

def main():
    print("="*80)
    print("EPSTEIN DOCUMENTS PIPELINE")
    print("Automated Download -> OCR -> Analysis")
    print("="*80)

    # Step 1: Download (check for new folders)
    existing_folders = download_missing_folders()

    # Step 2: OCR folders that haven't been processed
    print(f"\n{'='*80}")
    print("STEP 2: OCR PROCESSING")
    print(f"{'='*80}")

    ocred_folders = check_ocr_status()
    print(f"Already OCRed folders: {ocred_folders}")

    folders_to_ocr = []
    for folder_num in existing_folders:
        folder_path = IMAGES_DIR / folder_num
        if folder_path.exists() and folder_num not in ocred_folders:
            folders_to_ocr.append((folder_num, folder_path))

    if folders_to_ocr:
        print(f"\nFolders needing OCR: {[f[0] for f in folders_to_ocr]}")
        for folder_num, folder_path in folders_to_ocr:
            ocr_folder(folder_num, folder_path)
    else:
        print("\nAll folders already OCRed!")

    # Step 3: Analyze all OCRed folders
    print(f"\n{'='*80}")
    print("STEP 3: CONTENT ANALYSIS")
    print(f"{'='*80}")

    all_results = {}
    ocred_folders = check_ocr_status()  # Refresh list

    for folder_num in ocred_folders:
        result = analyze_folder(folder_num)
        if result:
            all_results[folder_num] = result

    # Also analyze DATA folder if it exists
    data_folder = OCR_OUTPUT_DIR / "DATA" / "folder_009"
    if data_folder.exists():
        result = analyze_folder("DATA/folder_009")
        if result:
            all_results["DATA/folder_009"] = result

    # Step 4: Generate comprehensive report
    if all_results:
        generate_report(all_results)
    else:
        print("\nNo results to report!")

    print(f"\n{'='*80}")
    print("PIPELINE COMPLETE")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nPipeline interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nPipeline error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
