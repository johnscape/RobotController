from objectData.rayTracer import DepthCamera
import cv2
import numpy as np
import math
from settings import Verbose
from robot.imgConverter import LoadFromDataFile
from networking.server import RobotServer
from networking.client import RobotClient
import time
from robot.controller import Robot

r = Robot()
r.Setup()
r.Start()