from Server.server import RobotServer
from Controller.robot.navigator import RobotNavigator
from Controller.imagery.ImageBuilder import ImageBuilder
from Controller.robot.imageProcessor import ImageProcessor

server = RobotServer(verbose=True)

imgBuilder = ImageBuilder()
imgProcessor = ImageProcessor(imgBuilder, server)
navigator = RobotNavigator(imgProcessor, server)

server.Start()
while not navigator.Stop:
    imgProcessor.ImageProcessorStep()
    navigator.NaviagtionStep()
