import cv2
import numpy as np

# Define a more detailed set of ASCII characters
ASCII_CHARS = "@#S%?*+;:,. "

def pixel_to_ascii(pixel_value):
    """Convert pixel value to an ASCII character."""
    return ASCII_CHARS[pixel_value * (len(ASCII_CHARS) - 1) // 255]

def frame_to_ascii(frame, width=120):
    """Convert a frame to ASCII art with higher definition."""
    # Convert frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Resize the frame to the desired width while maintaining aspect ratio
    height, orig_width = gray_frame.shape
    aspect_ratio = orig_width / float(height)
    new_height = int(width / aspect_ratio)
    resized_frame = cv2.resize(gray_frame, (width, new_height))
    
    # Convert each pixel to an ASCII character
    ascii_frame = "\n".join("".join(pixel_to_ascii(pixel) for pixel in row) for row in resized_frame)
    
    return ascii_frame

def main():
    # Open the default video camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Unable to open the camera")
        return
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert frame to ASCII art
        ascii_frame = frame_to_ascii(frame)
        
        # Clear the terminal
        print("\033c", end="")
        
        # Print the ASCII art to the terminal
        print(ascii_frame)
        
        # Exit on ESC key press
        if cv2.waitKey(1) == 27:
            break
    
    cap.release()

if __name__ == "__main__":
    main()
