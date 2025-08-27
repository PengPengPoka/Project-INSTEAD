import cv2 as cv
import os

class Camera:
    def __init__(self):
        self.cam_setting = {}

    def OpenSettings(self, filename):
        # with open(filename, 'r') as file:
        #     for line in file:
        #         variable, value = line.strip().split('=')
        #         self.cam_setting[variable.strip()] = int(value.strip())
        try:
            with open(filename, 'r') as file:
                for line in file:
                    parts = line.strip().split('=')
                    if len(parts) == 2:
                        variable = parts[0].strip()
                        value = parts[1].strip()
                        self.cam_setting[variable] = int(value)
                    else:
                        print(f"Ignoring malformed line: {line.strip()}")
        except FileNotFoundError:
            print(f"Configuration file not found: {filename}")
        except Exception as e:
            print(f"An error occurred while reading the configuration file: {str(e)}")


    def WriteSetting(self, filename):
        with open(filename, 'w') as file:
            for var, value in self.cam_setting.items():
                line = f"{var}={value}\n"
                file.write(line)

    # def getSettings(self):
    #     self.brightness = self.cam_setting['brightness']
    #     self.contrast = self.cam_setting['contrast']
    #     self.saturation = self.cam_setting['saturation']
    #     self.sharpness = self.cam_setting['sharpness']
    #     self.white_balance = self.cam_setting['white_balance']
    #     self.gain = self.cam_setting['gain']
    #     self.zoom = self.cam_setting['zoom']
    #     self.focus = self.cam_setting['focus'] 
    #     self.exposure = self.cam_setting['exposure']
    #     self.pan = self.cam_setting['pan']
    #     self.tilt = self.cam_setting['tilt']

    def getSettings(self):
        self.brightness = self.cam_setting.get('brightness', 0)
        self.contrast = self.cam_setting.get('contrast', 0)
        self.saturation = self.cam_setting.get('saturation', 0)
        self.sharpness = self.cam_setting.get('sharpness', 0)
        self.white_balance = self.cam_setting.get('white_balance', 0)
        self.gain = self.cam_setting.get('gain', 0)
        self.zoom = self.cam_setting.get('zoom', 0)
        self.focus = self.cam_setting.get('focus', 0) 
        self.exposure = self.cam_setting.get('exposure', 0)
        self.pan = self.cam_setting.get('pan', 0)
        self.tilt = self.cam_setting.get('tilt', 0) 

    def AutoOff(self, device):
        device.set(cv.CAP_PROP_AUTOFOCUS,0)
        device.set(cv.CAP_PROP_AUTO_WB,0)
        device.set(cv.CAP_PROP_AUTO_EXPOSURE,0)

    def setSettings(self, device):
        # self.tilt = self.cam_setting.get('tilt', 0)
        # device.set(cv.CAP_PROP_TILT, self.tilt)
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


    def CaptureImage(self, frame, img_name, ext):
        cv.imwrite(f"{img_name}.{ext}", frame)
        print(f"Image {img_name}.{ext} has been created")

    def setManualSettings(self, device, variable, value):
        device.set(variable, value)

    def applyConfig(self, settings, device):
        self.AutoOff(device)
        self.brightness = settings['brightness']
        self.contrast = settings['contrast']
        self.saturation = settings['saturation']
        self.sharpness = settings['sharpness']
        self.white_balance = settings['white_balance']
        self.gain = settings['gain']
        self.zoom = settings['zoom']
        self.focus = settings['focus'] 
        self.exposure = settings['exposure']
        self.pan = settings['pan']
        self.tilt = settings['tilt']

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

        print('Camera parameters applied!')



def main():
    cam = Camera()
    #home = os.path.expanduser("~")
    #path = os.path.join(home, "Repositories", "Project-INSTEAD", "vision", "default_param.txt")
    path = 'media/Backup/Teh/teststack/default_param.txt'
    cam.OpenSettings(path)

    cap = cv.VideoCapture(0, cv.CAP_DSHOW)

    if not cap.isOpened():
        print("No capture device")
        return
    cam.setSettings(cap)

    while cap.isOpened():
        grab, frame = cap.read()

        if not grab:
            print("Capture failed")
            break

        cv.imshow("video", frame)
        key = cv.waitKey(3)

        if key == 27:
            break

        elif key == 32:
            print("Spacebar key pressed. Entering image data collection mode")
            # img_name = input("Enter image name: ")
            # ext = input("Enter image extension (e.g., jpg): ")
            cam.CaptureImage(frame)

        elif key == 99:
            print("C key pressed. Entering manual mode setting")
            # variable = cv.CAP_PROP_TILT
            # value = int(input("Enter manual setting value: "))
            cam.setManualSettings(cap)

        elif key == 115:
            print("S key pressed. Saving camera setting")
            cam.WriteSetting()

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()
