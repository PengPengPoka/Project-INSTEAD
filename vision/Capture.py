import cv2 as cv    # opencv library
import threading    # multithreading library
import time

def capture(frame):     # capture function
    img_name = str(input("image name: "))
    extention = str(input("extention: "))
    cv.imwrite((img_name + "." + extention), frame)
    print("image " + img_name + "." + extention + " has been created")
    
def resolutionSetting(cap): # resolution setting function
    height = int(input("frame height: "))
    width = int(input("frame width: "))
    
    cap.set(cv.CAP_PROP_FRAME_HEIGHT,height)
    cap.set(cv.CAP_PROP_FRAME_WIDTH,width)

def exposureSetting(cap):
    expo = int(input("exposure value: "))
    cap.set(cv.CAP_PROP_AUTO_EXPOSURE,0)
    cap.set(cv.CAP_PROP_EXPOSURE, expo)

def focusSetting(cap):
    focus = float(input("focus value: "))
    cap.set(cv.CAP_PROP_AUTOFOCUS,0)
    cap.set(cv.CAP_PROP_FOCUS, focus)
    
def brightnessSetting(cap):
    bright = int(input("brightness value: "))
    cap.set(cv.CAP_PROP_BRIGHTNESS,bright)
    
def contrastSetting(cap):
    contrast = int(input("contrast value: "))
    cap.set(cv.CAP_PROP_CONTRAST,contrast)
    
def saturationSetting(cap):
    saturation = int(input("saturation value: "))
    cap.set(cv.CAP_PROP_SATURATION,saturation)
    
def hueSetting(cap):
    hue = int(input("hue value: "))
    cap.set(cv.CAP_PROP_HUE,hue)
    
def gainSetting(cap):
    gain = int(input("gain value: "))
    cap.set(cv.CAP_PROP_GAIN,gain)
    
def WBSetting(cap):
    wb = int(input("WB value: "))
    cap.set(cv.CAP_PROP_WB_TEMPERATURE,wb)

def main():
    cap = cv.VideoCapture(0)    # ambil index kamera

    resolutionSetting(cap)      # setting resolusi kamera
    cap.set(cv.CAP_PROP_AUTO_EXPOSURE,0)
    cap.set(cv.CAP_PROP_AUTO_WB,0)
    cv.namedWindow("webcam")    # window webcam
    cap.set(cv.CAP_PROP_SETTINGS,1)
    
    
    while cap.isOpened():
        
        grab,frame = cap.read()
        
        if not grab:    # cek apakah capture berhasil
            print("capture failed")
            break
        
        cv.imshow("webcam",frame)   # tampilan hasil capture
        key = cv.waitKey(3)
                
        if key == 27:   # 27 = escape key
            print("Escape button pressed. Exiting program!")
            break
        
        elif key == 101:    # 101 = e key
            print("E key pressed. Entering exposure setting")
            exposureSetting(cap)
            # tExposure.start()

        elif key == 102:    # 102 = f key
            print("F key pressed. Entering focus setting")
            focusSetting(cap)
            
        elif key == 98:
            print("B key pressed. Entering brightness setting")
            brightnessSetting(cap)
            
        elif key == 99:
            print("C key pressed. Entering contrast setting")
            contrastSetting(cap)
            
        elif key == 103:
            print("G key pressed. Entering gain setting")
            gainSetting(cap)
            
        elif key == 104:
            print("H key pressed. Entering hue setting")
            hueSetting(cap)
            
        elif key == 115:
            print("S key pressed. Entering saturation setting")
            saturationSetting(cap)
            
        elif key == 107:
            print("K key pressed. Entering WBU setting")
            WBSetting(cap)
        
        elif key == 32: # 32 = spacebar
            print("Spacebar key pressed. Entering image data collection")
            t1 = threading.Thread(target=capture,args=(frame,))     # thread buat capture gambar
            t1.start()
        
        cap.set(cv.CAP_PROP_AUTO_EXPOSURE,0)
        # if tExposure.is_alive() or tFocus.is_alive() == True:
        #     tExposure.join()
        #     tFocus.join()
            
    
if __name__ == "__main__":
    main()