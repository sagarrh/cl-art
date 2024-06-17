import cv2
import numpy as np
import ffmpeg

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
    # Capture the RTMP stream
    stream_url = 'rtmp://127.0.0.1/live'  # Replace with your RTMP server URL
    process = (
        ffmpeg
        .input(stream_url)
        .output('pipe:', format='rawvideo', pix_fmt='bgr24')
        .run_async(pipe_stdout=True)
    )

    width = 640
    height = 480

    while True:
        # Read a frame from the stream
        in_bytes = process.stdout.read(width * height * 3)
        if not in_bytes:
            break
        
        frame = (
            np
            .frombuffer(in_bytes, np.uint8)
            .reshape([height, width, 3])
        )
        
        # Convert frame to ASCII art
        ascii_frame = frame_to_ascii(frame)
        
        # Clear the terminal
        print("\033c", end="")
        
        # Print the ASCII art to the terminal
        print(ascii_frame)
        
if __name__ == "__main__":
    main()
