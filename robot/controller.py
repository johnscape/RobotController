from networking.client import RobotClient, CameraDirection
from networking.server import RobotServer
import cv2
import time
import os.path
import subprocess
import os
import numpy as np
import math

def DepthImageSmoothing(img, median):
    new_img = np.zeros((img.shape[0], img.shape[1], 3))
    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            values = []
            for xn in range(x - median, x + median + 1):
                if xn < 0 or xn >= img.shape[0]:
                    continue
                for yn in range(y - median, y + median + 1):
                    if yn < 0 or yn >= img.shape[0]:
                        continue
                    values.append(img[xn][yn][0])
            values.sort()
            if len(values) % 2 == 0:
                for c in range(3):
                    half = int(len(values) / 2)
                    new_img[x][y][c] = int((values[half] + values[half + 1]) / 2)
            else:
                for c in range(3):
                    new_img[x][y][c] = values[int((len(values) + 1) / 2)]
    return new_img

def ToBW(img):
    gray = np.reshape(img[:, :, 0], (img.shape[0], img.shape[1]))
    (thresh, bwImg) = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    return bwImg


def OpeningTransform(img, kernel_size):
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    img = cv2.erode(img, kernel)
    img = cv2.dilate(img, kernel)
    return img

def ClosingTransform(img, kernel_size):
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    img = cv2.dilate(img, kernel)
    img = cv2.erode(img, kernel)
    return img

class Robot:
    def __init__(self):
        self.Position = [0, 0, 0]
        self.Rotation = [0, 0, 0]
        self.Client = None
        self.Server = None
        self.CameraImg = None
        self.RobotWidth = 10
        self.Threshold = 30
        self.RobotSpeed = 5

    def Setup(self):
        self.Client = RobotClient()
        self.Server = RobotServer()

    def Start(self):
        self.Server.StartServer()
        time.sleep(1)
        self.Client.Connect()
        time.sleep(1)
        if not os.path.exists("DepthCamera\\bin\Debug\\DepthCamera.exe"):
            print("Camera application does not exists.")
            self.Server.StopServer()
            return
        print("Starting camera...")
        subprocess.Popen([r'DepthCamera\bin\Debug\DepthCamera.exe', '--S', '512', '--F', 'mesh.obj'], creationflags=subprocess.CREATE_NEW_CONSOLE)
        print("Waiting camera to load...")
        while (self.Client.Receive() != b'loaded'):
            time.sleep(1)
        print("Camera loaded, starting robot...")
        max_steps = 50000
        current_step = 0
        while current_step < max_steps:
            img = self.Client.BuildImage()
            rotate = False
            for x in range(self.RobotWidth):
                for y in range(img.shape[1]):
                    current_x = int((img.shape[0] / 2) + ((-self.RobotWidth / 2) + x))
                    if img[current_x][y][0] < self.Threshold:
                        rotate = True
                        break
                if rotate:
                    break
            if not rotate:
                self.Client.MoveCamera(CameraDirection.FORWARD, self.RobotSpeed)
            else:
                self.Client.MoveCamera(CameraDirection.ROTATE_LEFT, self.RobotSpeed * 10)
            #img = DepthImageSmoothing(img, 5)
            #
            #canny = cv2.Canny(img,100,200)
            #cv2.imshow("Canny", canny)

            '''
            bw = ToBW(img)
            o = OpeningTransform(img, 5) == 255
            c = ClosingTransform(img, 5) == 255
            segmentation = np.logical_and(o, c).astype(np.uint8) * 255
            
            '''

            bw = ToBW(img)
            o = OpeningTransform(bw, 5) == 255
            c = ClosingTransform(bw, 5) == 255
            segmentation = np.logical_and(o, c).astype(np.uint8) * 255
            segmentation = cv2.Canny(segmentation, 100, 200)

            _,alpha = cv2.threshold(segmentation,0,255,cv2.THRESH_BINARY)
            
            recolour = cv2.cvtColor(segmentation, cv2.COLOR_GRAY2BGR)
            recolour[:, :, 2] = np.zeros((recolour.shape[0], recolour.shape[1]))
            b, g, r = cv2.split(recolour)

            rgba = [b,g,r, alpha]
            dst = cv2.merge(rgba,4)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

            final = cv2.addWeighted(img, 1, dst, 1, 0)


            cv2.imshow("Robot view", final)
            cv2.waitKey(500)
            current_step += 1
        print("Robot movement finished!")


