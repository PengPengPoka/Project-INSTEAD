import cv2 as cv
import os

class Camera:
    def __init__(self):
        self.cam_setting = {}

    def OpenSettings(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                parts = line.strip().split('=')
                variable = parts[0].strip()
                value = parts[1].strip()

                self.cam_setting[variable] = int(value)

    def WriteSetting(self):
        filename = str(input("file name: "))

        self.cam_setting['brightness'] = self.brightness
        self.cam_setting['contrast'] = self.contrast
        self.cam_setting['saturation'] = self.saturation
        self.cam_setting['sharpness'] = self.sharpness
        self.cam_setting['white_balance'] = self.white_balance
        self.cam_setting['gain'] = self.gain
        self.cam_setting['zoom'] = self.zoom
        self.cam_setting['focus'] = self.focus
        self.cam_setting['exposure'] = self.exposure
        self.cam_setting['pan'] = self.pan
        self.cam_setting['tilt'] = self.tilt

        with open(filename, 'w') as file:
            for var, value in self.cam_setting.items():
                line = f"{var}={value}\n"
                file.write(line)

    def getSettings(self):
        self.brightness = self.cam_setting['brightness']
        self.contrast = self.cam_setting['contrast']
        self.saturation = self.cam_setting['saturation']
        self.sharpness = self.cam_setting['sharpness']
        self.white_balance = self.cam_setting['white_balance']
        self.gain = self.cam_setting['gain']
        self.zoom = self.cam_setting['zoom']
        self.focus = self.cam_setting['focus'] 
        self.exposure = self.cam_setting['exposure']
        self.pan = self.cam_setting['pan']
        self.tilt = self.cam_setting['tilt']

    def AutoOff(self, device):
        device.set(cv.CAP_PROP_AUTOFOCUS,0)
        device.set(cv.CAP_PROP_AUTO_WB,0)
        device.set(cv.CAP_PROP_AUTO_EXPOSURE,0)
        device.set(cv.CAP_PROP_AUTO_WB,1)

    def setSettings(self, device):
        self.AutoOff(device)
        self.getSettings()

        device.set(cv.CAP_PROP_BRIGHTNESS, self.brightness)
        device.set(cv.CAP_PROP_CONTRAST, self.contrast)
        device.set(cv.CAP_PROP_SATURATION, self.saturation)
        device.set(cv.CAP_PROP_SHARPNESS, self.sharpness)
        device.set(cv.CAP_PROP_WB_TEMPERATURE, self.white_balance)
        device.set(cv.CAP_PROP_GAIN, self.gain)
        device.set(cv.CAP_PROP_ZOOM, self.zoom)
        device.set(cv.CAP_PROP_FOCUS, self.focus)
        device.set(cv.CAP_PROP_EXPOSURE, self.exposure)
        device.set(cv.CAP_PROP_PAN, self.pan)
        device.set(cv.CAP_PROP_TILT, self.tilt)
        
    def CaptureImage(self, frame):
        img_name = str(input("image name: "))
        ext = str(input("extention: "))
        cv.imwrite((img_name + "." + ext), frame)
        print("image " + img_name + "." + ext + " has been created")

    def setManualSettings(self, device):
        print("Select mode:\n",
              "1. brightness\n",
              "2. contrast\n",
              "3. saturation\n",
              "4. sharpness\n",
              "5. white_balance\n",
              "6. gain\n",
              "7. zoom\n",
              "8. focus\n",
              "9. exposure\n",
              "10. pan\n",
              "11. tilt\n")
        
        mode = int(input("enter mode: "))

        if mode == 1:
            value = int(input("enter brightness value: "))
            self.brightness = value
            device.set(cv.CAP_PROP_BRIGHTNESS, self.brightness)
        
        elif mode == 2:
            value = int(input("enter contrast value: "))
            self.contrast = value
            device.set(cv.CAP_PROP_CONTRAST, self.contrast)
        
        elif mode == 3:
            value = int(input("enter saturation value: "))
            self.saturation = value
            device.set(cv.CAP_PROP_SATURATION, self.saturation)
        
        elif mode == 4:
            value = int(input("enter sharpness value: "))
            self.sharpness = value
            device.set(cv.CAP_PROP_SHARPNESS, self.sharpness)

        elif mode == 5:
            value = int(input("enter white balance value: "))
            self.white_balance = value
            device.set(cv.CAP_PROP_WB_TEMPERATURE, self.white_balance)

        elif mode == 6:
            value = int(input("enter gain value: "))
            self.gain = value
            device.set(cv.CAP_PROP_GAIN, self.gain)

        elif mode == 7:
            value = int(input("enter zoom value: "))
            self.zoom = value
            device.set(cv.CAP_PROP_ZOOM, self.zoom)

        elif mode == 8:
            value = int(input("enter focus value: "))
            self.focus = value
            device.set(cv.CAP_PROP_FOCUS, self.focus)

        elif mode == 9:
            value = int(input("enter exposure value: "))
            self.exposure = value
            device.set(cv.CAP_PROP_EXPOSURE, self.exposure)

        elif mode == 10:
            value = int(input("enter pan value: "))
            self.pan = value
            device.set(cv.CAP_PROP_PAN, self.pan)

        elif mode == 11:
            value = int(input("enter tilt value: "))
            self.tilt = value
            device.set(cv.CAP_PROP_TILT, self.tilt)


def main():
    cam = Camera()
    home = os.path.expanduser("~")
    path = home + "\\Repositories\\Project-INSTEAD\\vision\\default_param.txt"
    cam.OpenSettings(path)

    cap = cv.VideoCapture(0, cv.CAP_DSHOW)
    cam.setSettings(cap)

    if cap.isOpened() == False:
        print("no capture device")

    while cap.isOpened():
        grab, frame = cap.read()

        if not grab:
            print("capture failed")


        cv.imshow("video",frame)
        key = cv.waitKey(3)

        if key == 27:
            break

        elif key == 32:
            print("Spacebar key pressed. Entering image data collection mode")
            cam.CaptureImage(frame)

        elif key == 99:
            print("C key pressed. Entering manual mode setting")
            cam.setManualSettings(cap)

        elif key == 115:
            print("S key pressed. Saving camera setting")
            cam.WriteSetting()

if __name__ == "__main__":
    main()