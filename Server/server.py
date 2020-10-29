import socket
import sys
import logging
import threading
import time
from Server.LZW import LZW
import subprocess
import os

class RobotServer:
    def __init__(self, port=8008, verbose=False):
        self.Port = port
        self.IpAddress = "127.0.0.1"
        self.Socket = None
        self.Outgoing = []
        self.Incoming = []
        self.Communication = None
        self.Verbose = verbose
        self.Connection = None
        self.ClientAddress = None
        self.SendingMutex = threading.Lock()
        self.ReceivingMutex = threading.Lock()
        self.Decompressor = LZW()
        self.CameraAppPath = os.path.abspath("Camera/Debug/CameraController.exe")

    def Start(self):
        if not os.path.exists(self.CameraAppPath):
            logging.error("Camera application does not exists!")
            return
        self.Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Socket.bind((self.IpAddress, self.Port))
        if self.Verbose:
            logging.info("Waiting for camera to connect...")
        subprocess.Popen([self.CameraAppPath], creationflags=subprocess.CREATE_NEW_CONSOLE)
        self.Socket.listen(1)
        self.Connection, self.ClientAddress = self.Socket.accept()
        if self.Verbose:
            logging.info("Camera connected, starting communication.")
        self.Communication = threading.Thread(target=self.CommunicationLoop)
        self.Socket.settimeout(1)
        self.Communication.start()
        

    def CommunicationLoop(self):
        while True:
            try:
                data = self.Connection.recv(1024)
                #imgData = self.Decompressor.Decompress(data)
                #TODO: implement LZW
                imgData = data
                self.Incoming.append(imgData)
            except socket.timeout:
                continue
            if len(self.Outgoing) > 0:
                self.Connection.send(self.Outgoing[0])
                self.Outgoing.pop(0)

                


