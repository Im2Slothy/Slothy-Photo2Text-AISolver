import cv2
import numpy as np
import easyocr

# Initialize EasyOCR reader for English
reader = easyocr.Reader(['en'])

def preprocess_image_for_ocr(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Threshold the image using adaptive thresholding for better separation
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                  cv2.THRESH_BINARY_INV, 31, 2)
    
    # Morphological opening to remove small noise
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    
    # Erode lightly to thin characters without losing text
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    erosion = cv2.erode(opening, kernel, iterations=1)  # Reduced to 1 to preserve all text
    
    return erosion  # Return the processed image

def capture_text(cap):
    ret, frame = cap.read()
    if ret:
        processed_image = preprocess_image_for_ocr(frame)
        # Save the processed image for debugging
        cv2.imwrite("debug_processed_image.png", processed_image)
        
        # Use EasyOCR to read all text
        try:
            results = reader.readtext(processed_image, detail=0)  # detail=0 returns only text, not bounding boxes
            text = " ".join(results) if results else ""  # Join all detected text into a single string
        except Exception as e:
            print(f"EasyOCR error: {e}")
            text = ""
        
        return frame, text.strip()
    return None, None