import socket
import logging
import threading
import time
from networking.settings import UDP_PORT, UDP_IP

class RobotServer:
    def __init__(self):
        self.Running = False
        self.ServerThread = None
        self.ServerSocket = None

        self.CameraAddress = None
        self.RobotAddress = None

    def StartServer(self):
        logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
        self.Running = True
        self.ServerThread = threading.Thread(target=self.__ServerFunctions)
        self.ServerThread.start()

    def StopServer(self):
        if self.ServerThread is None:
            print("The server cannot be stopped, because it's not running.")
            return
        


    def __ServerFunctions(self):
        self.ServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.ServerSocket.bind((UDP_IP, UDP_PORT))
        logging.info("Server started!")

        while self.Running:
            bytesAddressPair = self.ServerSocket.recvfrom(1024)
            message = bytesAddressPair[0]
            address = bytesAddressPair[1]

            if self.RobotAddress is None and message[0] == 114:
                self.RobotAddress = address
                self.ServerSocket.sendto(str.encode("hello robot"), address)
            elif self.CameraAddress is None and message[0] == 99:
                self.CameraAddress = address
                self.ServerSocket.sendto(str.encode("hello camera"), address)

            if self.RobotAddress is not None and self.CameraAddress is not None:
                if message[0] == 114:
                    self.ServerSocket.sendto(message[1:], self.CameraAddress)
                elif message[0] == 99:
                    self.ServerSocket.sendto(message[1:], self.RobotAddress)

            if message == b'exit':
                break
        
        logging.info("Stopping server")

