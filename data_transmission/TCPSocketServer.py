from typing import Optional, List, Callable
import socket
import threading
import time

class TCPSocketServer(object):

    def __init__(self, port: int, host: str = "localhost", autostart: bool = True, chunkSize: int = 16):
        self.port = port
        self.host = host
        self.serverAddress = (host, port)
        self.chunkSize = chunkSize

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.Init()

        self.hookLock = threading.Lock()
        self.hooks: List[Callable] = list()

        self.thread = threading.Thread(target=self._run, args=())

        self.joinLock = threading.Lock()
        self.joinThread = False

        if autostart:
            self.Start()

    def Init(self):
        self.socket.bind(self.serverAddress)

    def Start(self):
        if not self.thread.is_alive():
            self.socket.listen()
            self.thread.start()

    def AddHook(self, myCallable: Callable):
        try:
            self.hookLock.acquire()
            self.hooks.append(myCallable)
        finally:
            self.hookLock.release()

    def RemoveHook(self, myCallable: Callable):
        try:
            self.hookLock.acquire()
            if self.hooks.__contains__(myCallable):
                self.hooks.remove(myCallable)
        finally:
            self.hookLock.release()

    def fireHooks(self, connection: any, data: List[bytes]):
        try:
            self.hookLock.acquire()

            for hook in self.hooks:
                hook(connection, data)

        finally:
            self.hookLock.release()

    def _run(self):
        print("Started TCP SocketServer on: " + self.host + ": " + str(self.port))
        _join = False
        try:
            self.joinLock.acquire()
            self.joinThread = False
        finally:
            self.joinLock.release()

        while not _join:
            connection, client_address = self.socket.accept()

            try:
                dataCollection : List[bytes] = []
                while True:
                    data = connection.recv(self.chunkSize)
                    if data:
                        dataCollection.append(data)
                    else:
                        self.fireHooks(connection, dataCollection)
                        break
            finally:
                # Clean up the connection
                connection.close()
                try:
                    self.joinLock.acquire()
                    _join = self.joinThread
                finally:
                    self.joinLock.release()

    def IsRunning(self):
        return self.thread.is_alive()

    def Stop(self):
        if self.thread.is_alive():
            try:
                self.joinLock.acquire()
                self.joinThread = True
            finally:
                self.joinLock.release()

            self.thread.join()

            while self.thread.is_alive():
                time.sleep(0.05)

            self.socket.close()
