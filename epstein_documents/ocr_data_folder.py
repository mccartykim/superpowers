#!/usr/bin/env python3
"""
OCR script for Epstein Estate Documents - DATA folder processing
Processes .dat and .opt files and performs OCR on associated images
"""

import os
import csv
import subprocess
import json
from pathlib import Path
from datetime import datetime

# Paths
BASE_DIR = Path("/home/user/superpowers/epstein_documents/Epstein Estate Documents - Seventh Production")
DATA_DIR = BASE_DIR / "DATA"
IMAGES_DIR = BASE_DIR / "IMAGES"
OUTPUT_DIR = Path("/home/user/superpowers/epstein_documents/ocr_results/DATA")

# Files
DAT_FILE = DATA_DIR / "HOUSE_OVERSIGHT_009.dat"
OPT_FILE = DATA_DIR / "HOUSE_OVERSIGHT_009.opt"

def parse_dat_file(dat_path):
    """Parse the Concordance DAT file (Þ delimited)"""
    print(f"Parsing DAT file: {dat_path}")

    records = []
    with open(dat_path, 'rb') as f:
        content = f.read().decode('utf-8', errors='ignore')

    # Split by record separator (Þ followed by newline)
    lines = content.split('\r\n')

    # First line is header
    if lines:
        header_line = lines[0]
        headers = header_line.split('Þ')[1:]  # Skip BOM
        headers = [h.replace('\x14', '').strip() for h in headers]

        print(f"Found {len(headers)} columns in DAT file")

        # Parse data rows
        for line in lines[1:]:
            if not line.strip():
                continue
            fields = line.split('Þ')[1:]  # Skip first empty field
            fields = [f.replace('\x14', '').replace('\r', '').strip() for f in fields]

            if len(fields) == len(headers):
                record = dict(zip(headers, fields))
                records.append(record)

    print(f"Parsed {len(records)} records from DAT file")
    return records, headers

def parse_opt_file(opt_path):
    """Parse the Opticon file (CSV with image paths)"""
    print(f"Parsing OPT file: {opt_path}")

    images = []
    with open(opt_path, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) >= 3:
                doc_id = parts[0]
                prod_id = parts[1]
                image_path = parts[2]
                images.append({
                    'doc_id': doc_id,
                    'prod_id': prod_id,
                    'image_path': image_path
                })

    print(f"Parsed {len(images)} image references from OPT file")
    return images

def ocr_image(image_path, output_path):
    """Run Tesseract OCR on an image"""
    try:
        # Tesseract command: output to text file
        result = subprocess.run(
            ['tesseract', str(image_path), str(output_path.with_suffix('')), '--dpi', '300'],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            # Read the generated text file
            txt_file = output_path.with_suffix('.txt')
            if txt_file.exists():
                with open(txt_file, 'r', encoding='utf-8') as f:
                    text = f.read()
                return True, text, None
            else:
                return False, "", "Output file not created"
        else:
            return False, "", result.stderr

    except subprocess.TimeoutExpired:
        return False, "", "OCR timeout (>60s)"
    except Exception as e:
        return False, "", str(e)

def process_folder_009():
    """Process all images in folder 009"""
    print("\n" + "="*80)
    print("PROCESSING FOLDER 009 IMAGES")
    print("="*80)

    folder_009 = IMAGES_DIR / "009"
    if not folder_009.exists():
        print(f"ERROR: Folder not found: {folder_009}")
        return []

    # Get all JPG files
    image_files = sorted(folder_009.glob("*.jpg"))
    print(f"Found {len(image_files)} images in folder 009")

    results = []
    output_folder = OUTPUT_DIR / "folder_009"
    output_folder.mkdir(parents=True, exist_ok=True)

    for i, image_path in enumerate(image_files, 1):
        print(f"\n[{i}/{len(image_files)}] Processing: {image_path.name}")

        # Create output path
        output_path = output_folder / image_path.stem

        # Run OCR
        success, text, error = ocr_image(image_path, output_path)

        result = {
            'image': image_path.name,
            'image_path': str(image_path),
            'output_path': str(output_path.with_suffix('.txt')),
            'success': success,
            'text_length': len(text) if success else 0,
            'error': error,
            'text_preview': text[:200] if success and text else ""
        }

        if success:
            print(f"  ✓ SUCCESS - Extracted {len(text)} characters")
            if text.strip():
                print(f"  Preview: {text[:100].strip()}...")
            else:
                print(f"  WARNING: No text extracted (blank page or image)")
        else:
            print(f"  ✗ FAILED - {error}")

        results.append(result)

    return results

def create_summary_report(dat_records, opt_images, ocr_results):
    """Create a comprehensive summary report"""
    print("\n" + "="*80)
    print("CREATING SUMMARY REPORT")
    print("="*80)

    # Overall statistics
    total_documents = len(dat_records)
    total_images = len(opt_images)
    total_ocr_processed = len(ocr_results)
    successful_ocr = sum(1 for r in ocr_results if r['success'])
    failed_ocr = total_ocr_processed - successful_ocr

    total_chars_extracted = sum(r['text_length'] for r in ocr_results if r['success'])

    # Find folder 009 documents in DAT
    folder_009_docs = [doc for doc in dat_records
                       if '\\009\\' in doc.get('Text Link', '') or
                          doc.get('Bates Begin', '').startswith('HOUSE_OVERSIGHT_026')]

    # Create report
    report = []
    report.append("="*80)
    report.append("EPSTEIN ESTATE DOCUMENTS - SEVENTH PRODUCTION")
    report.append("DATA FOLDER OCR ANALYSIS REPORT")
    report.append("="*80)
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")

    report.append("FILE ANALYSIS")
    report.append("-" * 80)
    report.append(f"DAT File: {DAT_FILE}")
    report.append(f"  - Total documents: {total_documents}")
    report.append(f"  - Format: Concordance DAT (Þ delimited)")
    report.append("")
    report.append(f"OPT File: {OPT_FILE}")
    report.append(f"  - Total image references: {total_images}")
    report.append(f"  - Format: Opticon CSV")
    report.append("")

    report.append("DOCUMENT STRUCTURE")
    report.append("-" * 80)
    if dat_records:
        sample_doc = dat_records[0]
        report.append("DAT File Fields:")
        for key in sample_doc.keys():
            value = sample_doc[key]
            if value:
                report.append(f"  - {key}: {value[:50]}...")
            else:
                report.append(f"  - {key}: (empty)")
    report.append("")

    report.append("FOLDER 009 ANALYSIS")
    report.append("-" * 80)
    report.append(f"Documents in folder 009: {len(folder_009_docs)}")
    report.append(f"Images processed: {total_ocr_processed}")
    report.append("")

    if folder_009_docs:
        report.append("Sample documents from folder 009:")
        for doc in folder_009_docs[:3]:
            report.append(f"  - Bates: {doc.get('Bates Begin', '')} - {doc.get('Bates End', '')}")
            report.append(f"    Pages: {doc.get('Pages', '')}")
            report.append(f"    Custodian: {doc.get('Custodian/Source', '')}")
            report.append(f"    Filename: {doc.get('Original Filename', '')}")
            report.append(f"    Date Created: {doc.get('Date Created', '')}")
            report.append("")

    report.append("OCR RESULTS")
    report.append("-" * 80)
    report.append(f"Images processed: {total_ocr_processed}")
    report.append(f"Successful: {successful_ocr} ({successful_ocr/total_ocr_processed*100:.1f}%)")
    report.append(f"Failed: {failed_ocr}")
    report.append(f"Total characters extracted: {total_chars_extracted:,}")
    report.append("")

    report.append("OCR DETAILED RESULTS")
    report.append("-" * 80)
    for result in ocr_results:
        status = "✓" if result['success'] else "✗"
        report.append(f"{status} {result['image']}")
        if result['success']:
            report.append(f"   Characters: {result['text_length']:,}")
            if result['text_preview']:
                report.append(f"   Preview: {result['text_preview'].strip()[:100]}...")
        else:
            report.append(f"   Error: {result['error']}")
        report.append("")

    report.append("="*80)
    report.append("KEY FINDINGS")
    report.append("="*80)
    report.append("")
    report.append("1. FILE FORMAT:")
    report.append("   - .DAT file is a Concordance DAT format (legal eDiscovery standard)")
    report.append("   - Uses Þ (thorn) character as field delimiter")
    report.append(f"   - Contains metadata for {total_documents} documents")
    report.append("")
    report.append("2. DOCUMENT COLLECTION:")
    report.append(f"   - Total images across all folders: {total_images}")
    report.append("   - Images are scanned at 300 DPI (good quality for OCR)")
    report.append("   - Documents span folders 001-009")
    report.append("")
    report.append("3. TEXT EXTRACTION:")
    report.append("   - The DAT file references TEXT files that don't exist yet")
    report.append("   - OCR is needed to extract text from the scanned images")
    report.append(f"   - Successfully extracted text from {successful_ocr}/{total_ocr_processed} images in folder 009")
    report.append("")
    report.append("4. CONTENT:")
    report.append("   - Documents appear to be from Jeffrey Epstein's estate")
    report.append("   - Includes PDFs, emails, and other document types")
    report.append("   - Date range appears to span 2011-2018")
    report.append("")

    report.append("="*80)
    report.append("END OF REPORT")
    report.append("="*80)

    report_text = "\n".join(report)

    # Save report
    report_path = OUTPUT_DIR / "ANALYSIS_REPORT.txt"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_text)

    print(f"\nReport saved to: {report_path}")
    print("\n" + report_text)

    # Also save JSON with detailed results
    json_path = OUTPUT_DIR / "ocr_results.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump({
            'summary': {
                'total_documents': total_documents,
                'total_images': total_images,
                'ocr_processed': total_ocr_processed,
                'ocr_successful': successful_ocr,
                'ocr_failed': failed_ocr,
                'total_chars_extracted': total_chars_extracted
            },
            'ocr_results': ocr_results,
            'folder_009_documents': [
                {k: v for k, v in doc.items() if v}  # Only include non-empty fields
                for doc in folder_009_docs
            ]
        }, f, indent=2)

    print(f"JSON results saved to: {json_path}")

def main():
    print("="*80)
    print("EPSTEIN ESTATE DOCUMENTS - DATA FOLDER OCR PROCESSOR")
    print("="*80)
    print()

    # Check Tesseract
    try:
        result = subprocess.run(['tesseract', '--version'], capture_output=True, text=True)
        print(f"Tesseract OCR found: {result.stdout.split()[1]}")
    except:
        print("ERROR: Tesseract not found! Please install: apt-get install tesseract-ocr")
        return

    # Parse DAT file
    dat_records, dat_headers = parse_dat_file(DAT_FILE)

    # Parse OPT file
    opt_images = parse_opt_file(OPT_FILE)

    # Process folder 009
    ocr_results = process_folder_009()

    # Create summary report
    create_summary_report(dat_records, opt_images, ocr_results)

    print("\n" + "="*80)
    print("PROCESSING COMPLETE!")
    print("="*80)
    print(f"\nOutput directory: {OUTPUT_DIR}")
    print(f"  - folder_009/: Individual OCR text files")
    print(f"  - ANALYSIS_REPORT.txt: Comprehensive summary")
    print(f"  - ocr_results.json: Detailed results in JSON format")

if __name__ == "__main__":
    main()
