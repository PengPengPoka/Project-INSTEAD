import cv2
import numpy as np
import os

# Global variables to store mouse click coordinates and cropping flag
center_x, center_y, radius = -1, -1, -1
cropping = False

# Mouse callback function
def mouse_callback(event, x, y, flags, param):
    global center_x, center_y, radius, cropping

    if event == cv2.EVENT_LBUTTONDOWN:
        center_x, center_y = x, y
        radius = 1  # Initialize radius to a small value
        cropping = True

    elif event == cv2.EVENT_MOUSEMOVE:
        if cropping:
            # Calculate the radius based on the mouse position
            radius = int(np.sqrt((x - center_x)**2 + (y - center_y)**2))

    elif event == cv2.EVENT_LBUTTONUP:
        cropping = False
        # Crop the circular region
        if radius > 0:
            cropped_region = image[
                max(0, center_y - radius):min(center_y + radius, image.shape[0]),
                max(0, center_x - radius):min(center_x + radius, image.shape[1])
            ]
            cv2.circle(image, (center_x,center_y),radius,[255,255,255],2)
            cv2.imshow("Cropped Image", cropped_region)

# Load an image
home = os.path.expanduser("~")
img_path = home + "\\OneDrive\\Pictures\\INSTEAD Teh\\DUST_2-1.jpg"
image = cv2.imread(img_path)  # Replace with your image path

# Create a window and set the mouse callback function
cv2.namedWindow("Image")
cv2.setMouseCallback("Image", mouse_callback)

while True:
    # Display the image
    cv2.imshow("Image", image)
    
    # Check for key press
    key = cv2.waitKey(1) & 0xFF
    
    # Exit loop if 'r' is pressed to reset the selection
    if key == ord("r"):
        center_x, center_y, radius = -1, -1, -1
        image = cv2.imread("your_image.jpg")  # Reload the original image
    
    # Exit loop if 'q' is pressed
    elif key == ord("q"):
        break

# Release resources and close windows
cv2.destroyAllWindows()
