# ocr_test.py
# (This script tests if EasyOCR is installed correctly and can read Japanese text)

import easyocr
import time

IMAGE_PATH = "test_image.png" 
# -----------------------------------------------------------


try:
    print("Loading EasyOCR model... (This may take a moment the first time)")
    start_time = time.time()
    reader = easyocr.Reader(['ja', 'en'], gpu=False) 
    print(f"Model loaded in {time.time() - start_time:.2f} seconds.")

except Exception as e:
    print(f"Error loading EasyOCR model: {e}")
    print("Please make sure 'easyocr' and 'torch' are installed correctly.")
    exit()


try:
    print(f"\nReading text from: {IMAGE_PATH}")
    results = reader.readtext(IMAGE_PATH, paragraph=True)

except FileNotFoundError:
    print(f"Error: Image file not found at '{IMAGE_PATH}'")
    print("Please check the IMAGE_PATH variable in the script.")
    exit()
except Exception as e:
    print(f"Error during OCR processing: {e}")
    exit()


if not results:
    print("--- OCR Results ---")
    print("No text detected in the image.")
else:
    print("\n--- OCR Results (Full Text) ---")
    
    full_text = " ".join([res[1] for res in results])
    
    print(full_text.strip())
    
    print("\n--- OCR Test Complete ---")