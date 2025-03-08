import cv2
import time
from src.ocr import capture_text
from src.api import query_gpt4, query_grok 
from src.display import display_results

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    last_frame = None
    captured_text = ""
    last_results = []

    # Print instructions and flush to ensure it displays
    print("Starting TripleCheckCam... Press SPACE to capture text, ESC to exit.", flush=True)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        # Display the webcam feed continuously
        cv2.imshow("TripleCheckCam", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == 32:  # SPACE key
            last_frame, captured_text = capture_text(cap)
            if captured_text:
                # Query both GPT-4 and Grok
                start_time = time.time()
                gpt4_response = query_gpt4(captured_text)
                gpt4_time = time.time() - start_time
                
                start_time = time.time()
                grok_response = query_grok(captured_text)
                grok_time = time.time() - start_time
                
                last_results = [gpt4_response, grok_response]
                display_results(last_frame, captured_text, last_results, print_to_console=True, show_continue_prompt=True)
        
        elif key == 27:  # ESC key
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
