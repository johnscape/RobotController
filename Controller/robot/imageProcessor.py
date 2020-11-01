from ..imagery.ImageBuilder import ImageBuilder
from Server.server import CameraOrders, RobotServer
import copy
import cv2
import numpy as np

class ImageProcessor:
    def __init__(self, imgBuilder: ImageBuilder, server: RobotServer):
        self.ImgBuilder = imgBuilder
        self.Server = server
        self.LastRGB = None
        self.LastDepth = None
        self.Stage = 0
        self.Ready = False
        #points of interest
        self.ClosestPoint = None

    def ImageProcessorStep(self):
        self.Ready = False
        if self.Stage == 0:
            self.Server.Outgoing.append(bytes([CameraOrders.TAKE_DEPTH.value]) + bytes(1))
            self.Stage += 1
            return
        elif self.Stage == 1:
            if len(self.Server.Incoming) > 0:
                self.ImgBuilder.Parts.append(self.Server.Incoming[0])
                self.Server.Incoming.pop(0)
            if not self.ImgBuilder.CanBuildDepth(): return
            self.LastDepth = self.ImgBuilder.BuildDepth(True)
            self.Stage += 1
            return
        elif self.Stage == 2:
            self.Server.Outgoing.append(bytes([CameraOrders.TAKE_RGB.value[0]]) + bytes(1))
            self.Stage += 1
            return
        elif self.Stage == 3:
            if len(self.Server.Incoming) > 0:
                self.ImgBuilder.Parts.append(self.Server.Incoming[0])
                self.Server.Incoming.pop(0)
            if not self.ImgBuilder.CanBuildRGB(): return
            self.LastRGB = self.ImgBuilder.BuildRGB(True)
            self.Stage += 1
            return
        elif self.Stage == 4:
            self.AnalyzeImage()
            self.Stage = 0
            self.Ready = True

    def AnalyzeImage(self):
        normalDepth = copy.deepcopy(self.LastDepth).astype(np.float32)
        normalDepth /= 255
        normalDepthBottom = normalDepth[256:][:]
        self.ClosestPoint = normalDepthBottom.min() #find the closest point to the camera