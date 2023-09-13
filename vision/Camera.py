import cv2 as cv

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


def main():
    cam = Camera()
    path = "C:\\Users\\ADMIN\\Repositories\\Project-INSTEAD\\vision\\default_param.txt"

    cam.OpenSettings(path)
    param = cam.cam_setting

    cam.getSettings()

    # print(param, brigthness)

if __name__ == "__main__":
    main()