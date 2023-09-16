import cv2 as cv

def main():
    cap = cv.VideoCapture(0,cv.CAP_DSHOW)
    cap.set(cv.CAP_PROP_SETTINGS,1)

    if cap.isOpened == False:
        print("no capture device detected")
    
    while cap.isOpened():
        grab, frame = cap.read()

        if not grab:
            print("capture failed")

        cv.imshow("video", frame)
        key = cv.waitKey(3)
        if key == 27:
            break

if __name__ == "__main__":
    main()