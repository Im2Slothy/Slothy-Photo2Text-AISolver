import cv2
import time
from src.ocr import capture_text
from src.api import query_grok  # Import only query_grok
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
                # Only query Grok since GPT-4 is commented out
                start_time = time.time()
                grok_response = query_grok(captured_text)
                end_time = time.time()
                grok_time = end_time - start_time
                
                # Simulate GPT-4 response since it's commented out
                gpt4_response = {"model": "GPT-4", "answer": "No API key provided (simulated)", "time": 0.01}
                
                last_results = [gpt4_response, grok_response]
                display_results(last_frame, captured_text, last_results, print_to_console=True, show_continue_prompt=True)
        
        elif key == 27:  # ESC key
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()