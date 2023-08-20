import cv2 as cv

def main():
    cap = cv.VideoCapture(0,cv.CAP_V4L)
    cap.set(3,640)
    cap.set(4,480)
    
    cap.set(cv.CAP_PROP_SETTINGS,1)
    
    if cap.isOpened() == False:
        print("capture device failed")
    else:
        while cap.isOpened():
            grab,img = cap.read()
            
            if not grab:
                print("capture failed")
            
            cv.imshow("video",img)
            key = cv.waitKey(3)
            
            if key==27:    # Esc key to stop
                break
            elif key==-1:  # normally -1 returned,so don't print it
                continue
            else:
                print(key) # else print its value
    
if __name__ == "__main__":
    main()