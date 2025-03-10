import cv2
import os

# Define the directory to save images
save_dir = "captured_images"
os.makedirs(save_dir, exist_ok=True)  # Create directory if it doesn't exist

## Initialize USB webcam (change 1 to 2 if it doesn't work)
cap = cv2.VideoCapture(2)

if not cap.isOpened():
    print("Error: Could not open any webcam.")
    exit()

count = 1

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture image.")
        break

    cv2.imshow('USB Webcam Capture', frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == 13:  # Press Enter to save image
        filename = os.path.join(save_dir, f"usb_capture_{count}.jpg")
        cv2.imwrite(filename, frame)
        print(f"Image saved: {filename}")
        count += 1
    elif key == ord('q'):  # Press 'q' to quit
        break

cap.release()
cv2.destroyAllWindows()
