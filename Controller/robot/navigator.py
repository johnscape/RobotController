from .imageProcessor import ImageProcessor
from Server.server import CameraOrders, RobotServer

class RobotNavigator:
    def __init__(self, imgProcessor: ImageProcessor, server: RobotServer):
        self.ImgProcessor = imgProcessor
        if imgProcessor is None:
            self.ImgProcessor = ImageBuilder()
        self.Server = server
        self.DepthNeeded = False
        self.Stop = False
        self.OrderSent = False
        self.ClosenessThreshold = 0.2

    def NaviagtionStep(self):
        if not self.ImgProcessor.Ready: return
        if self.ImgProcessor.ClosestPoint < self.ClosenessThreshold:
            print("Turning right")
            self.Server.Outgoing.append(bytes([CameraOrders.TURN_RIGHT.value[0]]) + bytes(1))
        else:
            print("Moving forward")
            self.Server.Outgoing.append(bytes([CameraOrders.MOVE_FORWARD.value[0]]) + bytes(1))
