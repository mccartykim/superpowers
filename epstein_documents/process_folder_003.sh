#!/bin/bash

SOURCE_DIR="/home/user/superpowers/epstein_documents/Epstein Estate Documents - Seventh Production/IMAGES/003"
OUTPUT_DIR="/home/user/superpowers/epstein_documents/ocr_results/003"

success_count=0
error_count=0
errors=""

cd "$SOURCE_DIR"

for img in *.jpg; do
    if [ -f "$img" ]; then
        base=$(basename "$img" .jpg)
        echo "Processing $img..."

        if tesseract "$img" "$OUTPUT_DIR/$base" 2>&1; then
            ((success_count++))
        else
            ((error_count++))
            errors+="Failed: $img\n"
        fi
    fi
done

echo ""
echo "================================"
echo "OCR Processing Complete"
echo "================================"
echo "Successfully processed: $success_count files"
echo "Errors: $error_count files"
if [ -n "$errors" ]; then
    echo -e "\nError details:\n$errors"
fi
