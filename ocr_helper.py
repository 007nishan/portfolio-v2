import pytesseract
from PIL import Image
import dateparser
import re
import os

def extract_challenge_info(image_path):
    """
    Extracts the date and/or title from an FCC challenge image using OCR.
    Target format: "For Wednesday September 17, 2025"
    """
    if not os.path.exists(image_path):
        return None, None

    try:
        # Perform OCR
        text = pytesseract.image_to_string(Image.open(image_path))
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        extracted_date_id = None
        extracted_title = None

        # 1. Try to find the date line
        # Pattern: something like "September 17, 2025"
        for line in lines:
            # Look for month names
            month_match = re.search(r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}', line, re.IGNORECASE)
            if month_match:
                date_str = month_match.group(0)
                parsed_date = dateparser.parse(date_str)
                if parsed_date:
                    extracted_date_id = parsed_date.strftime('%Y-%m-%d')
                    break
        
        # 2. Try to find the title line (usually follows "Challenge" or is at the top)
        # For simplicity, we'll look for the first line that isn't "Daily Coding Challenge" 
        # or the date line.
        for line in lines:
            if "Daily Coding Challenge" in line or "For " in line or extracted_date_id and any(m in line for m in ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]):
                continue
            if len(line) > 3 and not line.startswith('«'): # Usually titles are prominent
                extracted_title = line
                break

        return extracted_date_id, extracted_title

    except Exception as e:
        print(f"Error in OCR extraction: {e}")
        return None, None

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        d, t = extract_challenge_info(sys.argv[1])
        print(f"DATE_ID: {d}")
        print(f"TITLE: {t}")
