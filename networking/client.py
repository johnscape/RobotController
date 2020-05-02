import socket
from networking.settings import UDP_IP, UDP_PORT

class RobotClient:
    def __init__(self):
        self.ClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    def SendMsg(self, msg):
        byteData = str.encode(msg)
        self.ClientSocket.sendto(byteData, (UDP_IP, UDP_PORT))
