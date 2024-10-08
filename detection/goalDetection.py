import cv2
import numpy as np

def detect_goals(image_path):
    # Load the image
    image = cv2.imread(image_path)
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply edge detection
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    
    # Detect lines using Hough Line Transform
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10)

    # Initialize list to hold the coordinates of the goal posts
    goal_coordinates = []

    # Loop over detected lines to find the two goals
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            
            # Append start and end points of each detected line
            goal_coordinates.append((x1, y1, x2, y2))
            
            # Check if we found two lines, assuming these are the goals
            if len(goal_coordinates) >= 2:
                break

    # If exactly two goals are detected, return the coordinates
    if len(goal_coordinates) == 2:
        # Each goal has start and end point: [(x1, y1, x2, y2), (x3, y3, x4, y4)]
        return goal_coordinates[0], goal_coordinates[1]
    else:
        print("Goals not detected properly.")
        return None, None

# Example usage
goal1, goal2 = detect_goals('soccer_field.png')
if goal1 and goal2:
    print(f"Goal 1 Coordinates: Start({goal1[0]}, {goal1[1]}), End({goal1[2]}, {goal1[3]})")
    print(f"Goal 2 Coordinates: Start({goal2[0]}, {goal2[1]}), End({goal2[2]}, {goal2[3]})")
else:
    print("Could not detect both goals.")
