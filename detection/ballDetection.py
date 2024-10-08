import cv2
import pyautogui
import numpy as np

def detect_soccer_ball(image_path):
    # Load the image
    image = cv2.imread(image_path)
    
    # Convert to HSV color space for better color segmentation
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Define the color range for the soccer ball (adjust values as needed)
    # These values will depend on the ball's color in the game
    lower_color = np.array([20, 100, 100])  # Example for yellow ball
    upper_color = np.array([30, 255, 255])  # Example for yellow ball
    
    # Create a mask for the color range
    mask = cv2.inRange(hsv, lower_color, upper_color)
    
    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Initialize variables for the ball's coordinates
    ball_x, ball_y = None, None
    
    if contours:
        # Assume the largest contour is the ball
        largest_contour = max(contours, key=cv2.contourArea)
        
        # Compute the center of the largest contour
        M = cv2.moments(largest_contour)
        if M["m00"] != 0:
            ball_x = int(M["m10"] / M["m00"])
            ball_y = int(M["m01"] / M["m00"])
            
    return ball_x, ball_y

# Take a screenshot and save it
screenshot = pyautogui.screenshot()
screenshot.save("CurrentGame.jpg")

# Detect the soccer ball's coordinates
ball_x, ball_y = detect_soccer_ball("CurrentGame.jpg")
print(f"Soccer Ball Coordinates: ({ball_x}, {ball_y})")

# Optional: Display the image with the soccer ball marked
if ball_x is not None and ball_y is not None:
    image = cv2.imread("CurrentGame.jpg")
    cv2.circle(image, (ball_x, ball_y), 10, (0, 255, 0), -1)  # Draw a green circle on the ball
    cv2.imshow("Soccer Ball Detection", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Soccer ball not detected.")
