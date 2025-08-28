import cv2 as cv

def nothing():
    pass

def main():
    cap = cv.VideoCapture(0,cv.CAP_DSHOW)
    cap.set(cv.CAP_PROP_AUTO_WB,0)
    # cap.set(cv.CAP_PROP_SETTINGS,1)

    # cv.namedWindow("trackbar")
    # cv.createTrackbar("white balance", "trackbar", 2500, 6500, nothing)

    if cap.isOpened == False:
        print("no capture device detected")
    
    while cap.isOpened():
        grab, frame = cap.read()

        if not grab:
            print("capture failed")

        # white_balance = cv.getTrackbarPos("white balance", "trackbar")
        # cap.set(cv.CAP_PROP_WHITE_BALANCE_BLUE_U,25000)
        # cap.set(cv.CAP_PROP_WHITE_BALANCE_RED_V, 8000)
        cap.set(cv.CAP_PROP_WB_TEMPERATURE, 500)
        # print(white_balance)

        cv.imshow("video", frame)
        key = cv.waitKey(3)
        if key == 27:
            break

if __name__ == "__main__":
    main()