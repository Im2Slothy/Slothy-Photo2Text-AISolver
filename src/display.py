import cv2

def display_results(frame, question, answers, print_to_console=True, show_continue_prompt=False):
    # Print to console only if print_to_console is True
    if print_to_console:
        print("TRIPLE CHECK RESULTS", flush=True)
        print(f"Q: {question}", flush=True)
        
        # Extract answers for comparison
        answer_map = {result["model"]: result["answer"] for result in answers}
        times = {result["model"]: result["time"] for result in answers}
        
        # Print individual model results with times
        for model in sorted(answer_map.keys()):
            print(f"{model}: {answer_map[model]} ({times[model]:.2f}s)", flush=True)
        
        # Check for disagreement (simplified for Grok and GPT-4 only)
        has_disagreement = len(set(answer_map.values())) > 1  # More than one unique answer
        
        if has_disagreement:
            print("?????? Models disagree - check console", flush=True)
            print("\n" + "-"*50 + "\n", flush=True)
        else:
            print("All models agree\n" + "-"*50 + "\n", flush=True)

        # Add continuation prompt if requested
        if show_continue_prompt:
            print("(Triple Check - Press Space to continue)", flush=True)

    # Draw text directly on the frame (no blending)
    y_offset = 50
    cv2.putText(frame, "TRIPLE CHECK RESULTS", (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)  # Green
    y_offset += 40
    cv2.putText(frame, f"Q: {question[:50]}...", (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)  # White
    y_offset += 40
    for result in answers:
        text = f"{result['model']}: {result['answer']} ({result['time']:.2f}s)"
        cv2.putText(frame, text, (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)  # White
        y_offset += 30
    if len(set(result["answer"] for result in answers)) > 1:  # Check for disagreement in GUI
        cv2.putText(frame, "?????? Models disagree - check console", (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)  # Blue
        y_offset += 30
    if show_continue_prompt:
        cv2.putText(frame, "(Triple Check - Press Space to continue)", (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)  # Yellow