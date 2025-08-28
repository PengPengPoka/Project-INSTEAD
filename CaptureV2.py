import cv2 as cv

# Create a dictionary to store the settings
settings = {}

# Open the file for reading
with open('camera_param.txt', 'r') as file:
    for line in file:
        # Split each line into a variable and a value
        parts = line.strip().split('=')
        if len(parts) == 2:
            variable = parts[0].strip()
            value = parts[1].strip()
            
            # Store the variable and its corresponding value in the dictionary
            settings[variable] = int(value)  # Convert the value to an integer

# Now you can access the values by their variable names
focus = settings.get('focus')
exposure = settings.get('exposure')

# Print the values
print(f"Focus: {focus}")
print(f"Exposure: {exposure}")

def setFocus(cap):
    cap.set(cv.CAP_PROP_AUTOFOCUS,0)
    cap.set(cv.CAP_PROP_FOCUS,focus)

cap = cv.VideoCapture(1,cv.CAP_DSHOW)

while cap.isOpened:
    grab, frame = cap.read()

    if not grab:
        print("capture failed")

    setFocus(cap)

    cv.imshow("Webcam",frame)
    key = cv.waitKey(3)

    if key == 27:
        break