import time
from typing import List, Callable
import asyncio
from websocket import create_connection
from threading import Thread, Event, Lock

class WebsocketClient(object):

    def __init__(self, port: int, host: str="localhost", endpoint: str ="/", autoConnect: bool=True):
        self.thread: Thread = Thread(target=self._start, daemon=False)
        self.eventLoop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
        self.port: int = port
        self.uri = "ws://" + host + ":" + str(port) + endpoint

        self.messageLock = Lock()
        self.messages = list()

        self.disconnect = False

        self.dataReceivedHandler: List[Callable] = list()

        if autoConnect:
            self.Connect()

    def Connect(self):
        if not self.thread.is_alive():
            self.disconnect = False
            self.thread.start()

    def Stop(self):
        while self.thread.is_alive():
            self.disconnect = True
            time.sleep(0.5)


    def _start(self):
        ws = create_connection(self.uri, timeout=0.25)
        while not self.disconnect and ws.connected:
            try:
                self.messageLock.acquire()
                for msg in self.messages:
                    ws.send(msg)
                self.messages.clear()
            finally:
                self.messageLock.release()

            try:
                message = ws.recv()
                for callback in self.dataReceivedHandler:
                    callback(ws, message)
            except:
                pass

        ws.close()

    def Send(self, data: str):
        try:
            self.messageLock.acquire()
            self.messages.append(data)
        finally:
            self.messageLock.release()

