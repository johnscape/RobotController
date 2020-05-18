from networking.client import RobotClient, CameraDirection
from networking.server import RobotServer
import cv2
import time
import os.path
import subprocess
import os

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
            cv2.imshow("Robot view", img)
            cv2.waitKey(500)



