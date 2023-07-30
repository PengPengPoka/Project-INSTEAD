import cv2 as cv    # opencv library
import threading    # multithreading library

def capture(frame):     # capture function
    img_name = str(input("image name: "))
    extention = str(input("extention: "))
    cv.imwrite((img_name + "." + extention), frame)
    print("image " + img_name + "." + extention + " has been created")

def main():
    cap = cv.VideoCapture(0)    # ambil index kamera
    cv.namedWindow("webcam")    # window webcam
    
    while cap.isOpened():
        grab,frame = cap.read()
        t1 = threading.Thread(target=capture,args=(frame,))     # thread buat capture gambar
        
        if not grab:    # cek apakah capture berhasil
            print("capture failed")
            break
        
        cv.imshow("webcam",frame)   # tampilan hasil capture
        key = cv.waitKey(3)
        
        if key == 27:   # 27 = escape key
            print("Escape button pressed. Exiting program!")
            break
        
        elif key == 32: # 32 = spacebar
            print("Spacebar key pressed. Entering image data collection")
            t1.start()
            
    
if __name__ == "__main__":
    main()