import socket
from networking.settings import UDP_IP, UDP_PORT
from enum import Enum
import time
from collections import deque
import struct
import numpy as np
import cv2
import math

IMAGE_SIZE = 512

class CameraDirection(Enum):
    UP = 1,
    DOWN = 2,
    LEFT = 3,
    RIGHT = 4,
    FORWARD = 5,
    BACKWARD = 6


class RobotClient:
    def __init__(self):
        self.ClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    def SendMsg(self, msg):
        self.SendData(str.encode(msg))

    def SendData(self, msg):
        self.ClientSocket.sendto(msg, (UDP_IP, UDP_PORT))

    def MoveCameraUp(self, dist = 1):
        n_dist = dist % 255
        data = b'\x01' + bytes([n_dist])
        self.SendData(data)

    def MoveCameraDown(self, dist = 1):
        n_dist = dist % 255
        data = b'\x02' + bytes([n_dist])
        self.SendData(data)

    def MoveCamera(self, direction: CameraDirection, distance = 1):
        n_dist = dist % 255
        data = bytes([direction.value[0]]) + bytes([n_dist])
        self.SendData(data)

    def DiscardMsg(self):
        self.ClientSocket.recvfrom(1024)

    def Receive(self):
        self.SendData(b'get')
        data, addr = self.ClientSocket.recvfrom(1024) #mivel az első bájt le van vágva
        return data

    def BuildImage(self):
        image_count = math.ceil((IMAGE_SIZE * IMAGE_SIZE * 3) / 1024)
        fragments = deque([])
        full_data = b''
        tries = 0
        data_parts = 0
        while data_parts < image_count:
            data = self.Receive()
            if data == b'\x00':
                tries += 1
                if tries > 20 and data_parts == image_count - 1:
                    print("Cannot get last line, replicating")
                    full_data += full_data[-1023:]
                    data_parts += 1
                continue
            data_parts += 1
            full_data += data

        image = np.zeros((IMAGE_SIZE, IMAGE_SIZE, 3))
        for x in range(IMAGE_SIZE):
            for y in range(IMAGE_SIZE):
                for c in range(3):
                    current_val = full_data[3 * y + c + IMAGE_SIZE * 3 * x]
                    image[x][y][c] = current_val
        

        image = cv2.flip(image, 0)
        #cv2.imwrite('color_img.jpg', image)
        print("Image created!")
        return image


