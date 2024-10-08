import cv2
import pyautogui

screenshot = pyautogui.screenshot()
screenshot.save("CurrentGame.jpg")

# Load image from the file
image = cv2.imread("CurrentGame.jpg")