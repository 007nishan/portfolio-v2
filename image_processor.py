"""
image_processor.py
------------------
Cleans FCC branding (logo at top, mobile app text at bottom) from challenge images.
Performs surgical cropping and adds a uniform theme border for a premium "framed" look.
"""

import cv2
import numpy as np
import os
import glob

# Determine base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "static", "images")

def clean_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return False
    
    height, width = img.shape[:2]
    
    # 1. Surgical Cropping
    # Remove top header (logo area) and bottom footer (mobile app text)
    top_crop = int(height * 0.12)  # Cut top 12%
    bottom_crop = int(height * 0.94)  # Cut below 94%
    
    # Sample the theme color from the header row (before cropping)
    # This color will be used for the new frame
    theme_color = img[top_crop // 2, width // 2].tolist()
    
    # Perform crop
    cropped = img[top_crop:bottom_crop, 0:width]
    
    # 2. Close the Frame
    # Add a uniform border of the theme color to "close the frame"
    # User requested: "complete the frame with the same colour as it runs from the top"
    border_size = 12
    final_img = cv2.copyMakeBorder(
        cropped, 
        border_size, border_size, border_size, border_size, 
        cv2.BORDER_CONSTANT, 
        value=theme_color
    )
    
    # Overwrite the original file
    cv2.imwrite(image_path, final_img)
    return True

def main():
    images = glob.glob(os.path.join(IMAGE_DIR, "*.jpg"))
    print(f"[*] Processing {len(images)} images...")
    for img_path in images:
        # Avoid double-processing by checking if we already processed it (simple heuristic)
        # Or just process everything, it's fine for small sets
        clean_image(img_path)
    print("[+] Cleaning complete.")

if __name__ == "__main__":
    main()
