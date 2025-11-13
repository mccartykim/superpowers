#!/usr/bin/env python3
"""Script to download files from a Google Drive shared folder."""

import os
import sys
import gdown

def main():
    folder_url = "https://drive.google.com/drive/folders/1hTNH5woIRio578onLGElkTWofUSWRoH_"
    output_dir = "google_drive_files"

    print(f"Downloading files from Google Drive to {output_dir}...")

    try:
        # Use gdown to download the entire folder
        gdown.download_folder(
            url=folder_url,
            output=output_dir,
            quiet=False,
            use_cookies=False
        )
        print(f"\nDownload complete! Files saved to: {output_dir}")

    except Exception as e:
        print(f"Error downloading folder: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
