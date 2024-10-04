import pyautogui
import cv2


screenshot = pyautogui.screenshot()
screenshot.save("CurrentGame.jpg")

# Load image from the file
image = cv2.imread("CurrentGame.jpg")