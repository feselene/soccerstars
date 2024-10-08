import cv2
import pytesseract
import numpy as np

# Path to Tesseract executable, adjust it based on your installation
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update the path for your system

# Function to detect score from the image
def detect_score(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Preprocess the image: Convert to grayscale and apply threshold
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    # Define the regions of interest (ROIs) for the scores
    # You might need to adjust these coordinates based on where the scores appear on the screen
    # Assuming two regions: one for each player's score
    # Sample video: https://www.youtube.com/watch?v=hpd1ji3e-5Y
    score_region_player_1 = thresh[50:150, 50:200]  # Adjust coordinates
    score_region_player_2 = thresh[50:150, 300:450]  # Adjust coordinates

    # Apply OCR to detect the numbers in the ROIs
    score_player_1 = pytesseract.image_to_string(score_region_player_1, config='--psm 6 digits')
    score_player_2 = pytesseract.image_to_string(score_region_player_2, config='--psm 6 digits')

    # Clean up the OCR results (remove non-numeric characters)
    score_player_1 = ''.join(filter(str.isdigit, score_player_1))
    score_player_2 = ''.join(filter(str.isdigit, score_player_2))

    # Display the results
    print(f"Player 1 Score: {score_player_1}")
    print(f"Player 2 Score: {score_player_2}")

    # Optional: Show the regions of interest for debugging
    cv2.imshow('Player 1 Score', score_region_player_1)
    cv2.imshow('Player 2 Score', score_region_player_2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return score_player_1, score_player_2

# Example usage
image_path = 'path_to_screenshot.png'  # Replace with the path to your screenshot
detect_score(image_path)
