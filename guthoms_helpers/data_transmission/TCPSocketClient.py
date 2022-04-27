from typing import Optional, List, Callable
import socket
import threading
import time

class TCPSocketClient(object):

    def __init__(self, port: int, host: str = "localhost", autoconnect: bool = True, chunkSize: int = 16):
        self.port = port
        self.host = host
        self.serverAddress = (host, port)

        self.chunkSize = chunkSize

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.Init()

        self.isConnected = False

        if autoconnect:
            self.Connect()

    def Init(self):
        pass

    def Connect(self):
        self.socket.connect(self.serverAddress)
        self.isConnected = True
        pass

    def SendAll(self, data: bytearray):
        wasConnected = self.IsConnected()
        if not wasConnected:
            self.Connect()

        self.socket.sendall(data)

        if not wasConnected:
            self.Disconnect()

    def IsConnected(self):
        return self.isConnected

    def Disconnect(self):
        if self.isConnected:
            self.socket.close()
            self.isConnected = False
