import cv2
import numpy as np

def detect_player_coordinates(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert to grayscale for processing
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Threshold or color filtering to isolate players (adjust parameters as needed)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

    # Find contours to detect players
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # List to hold the coordinates of all detected players
    player_coordinates = []

    # Process each detected contour
    for contour in contours:
        # Compute the bounding box for each contour
        x, y, w, h = cv2.boundingRect(contour)
        
        # Calculate the center of the player
        center_x = x + w // 2
        center_y = y + h // 2
        
        # Add the player's center coordinates to the list
        player_coordinates.append((center_x, center_y))

    # Return the list of coordinates
    return player_coordinates

# Example usage
player_positions = detect_player_coordinates('soccer_field.png')
print("Player Coordinates:", player_positions)

# Optional: Draw detected player positions on the image for verification
image = cv2.imread('soccer_field.png')
for (x, y) in player_positions:
    cv2.circle(image, (x, y), 5, (0, 255, 0), -1)  # Draw green dots on players' positions

# Display the image with detected player positions
cv2.imshow("Player Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
