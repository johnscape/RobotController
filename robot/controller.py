from objectData.rayTracer import DepthCamera
from objectData.objectView import Verticle
import math
import numpy as np

class Robot:
    def __init__(self):
        self.Position = Verticle(0, 0, 0)
        self.Rotation = 0 # in degrees
        self.RotationVector = Verticle(1, 0, 0)
        self.Camera = None
        self.CameraResolution = [256, 256]

    def Rotate(self, value):
        self.Rotation = (self.Rotation + value) % 360
        self.RotationVector.X = math.cos(np.radians(self.Rotation))
        self.RotationVector.Y = math.sin(np.radians(self.Rotation))

    def Setup(self, building_file):
        self.Camera = DepthCamera()
        self.Camera.Object.LoadFile(building_file)
        self.Camera.ViewDegree = 90
        self.Camera.ViewPlaneSize = self.CameraResolution

    def Render(self):
        if self.Camera is None:
            print("Robot setup is not complete!")
            return
        self.Camera.ViewPoint = self.Position
        self.Camera.ViewDirection = self.RotationVector
        render = self.Camera.Render()