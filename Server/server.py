import socket
import sys
import logging
import threading
import time
import LZW

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
        self.Decompressor = LZW.LZW()

    def Start(self):
        self.Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Socket.bind((self.IpAddress, self.Port))
        if self.Verbose:
            logging.info("Waiting for camera to connect...")
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
                imgData = self.Decompressor.Decompress(data)

            except socket.timeout:
                continue

                


