import cv2
import numpy as np
import math

def get_arrow_length_and_angle(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert to grayscale for processing
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use edge detection to find lines in the image
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # Use HoughLinesP to detect lines (good for straight arrows)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=50, minLineLength=50, maxLineGap=10)

    # Check if any lines were found
    if lines is not None:
        # Assuming the first detected line is the arrow
        x1, y1, x2, y2 = lines[0][0]

        # Draw the line on the image for visualization
        cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Calculate the length of the arrow
        length = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        # Calculate the angle of the arrow in degrees
        angle = math.degrees(math.atan2(y2 - y1, x2 - x1))

        return length, angle
    else:
        print("No arrow detected.")
        return None, None

# Example usage
length, angle = get_arrow_length_and_angle('screenshot.png')
if length is not None and angle is not None:
    print(f"Arrow Length: {length}")
    print(f"Arrow Angle: {angle} degrees")

    # Display the image with detected arrow
    image = cv2.imread('screenshot.png')
    cv2.imshow("Arrow Detection", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Arrow could not be detected.")
