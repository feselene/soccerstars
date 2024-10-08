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

    # List to hold coordinates of detected players
    player_coordinates = []

    # Process each detected contour and collect up to 10 player coordinates
    for contour in contours:
        if len(player_coordinates) >= 10:
            break
        
        # Compute the bounding box for each contour
        x, y, w, h = cv2.boundingRect(contour)
        
        # Calculate the center of the player
        center_x = x + w // 2
        center_y = y + h // 2
        
        # Add the player's center coordinates to the list
        player_coordinates.extend([center_x, center_y])

    # Ensure exactly 10 players are detected, else pad with None or repeat last known
    while len(player_coordinates) < 20:
        player_coordinates.extend([None, None])

    return player_coordinates[:20]  # Return exactly 10 pairs of coordinates

# Example usage
player_positions = detect_player_coordinates('soccer_field.png')
print("Player Coordinates (10 players):", player_positions)

# Optional: Draw detected player positions on the image for verification
image = cv2.imread('soccer_field.png')
for i in range(0, len(player_positions), 2):
    if player_positions[i] is not None and player_positions[i+1] is not None:
        cv2.circle(image, (player_positions[i], player_positions[i+1]), 5, (0, 255, 0), -1)

# Display the image with detected player positions
cv2.imshow("Player Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
