from typing import Optional, Dict, List, Callable
import asyncio
import time
import websockets
from asyncio.futures import Future
import signal
from threading import Thread, Event, Lock

class WebsocketServer(object):

    def __init__(self, port: int, autostart: bool=True, waitForStartup: bool=True):
        self.thread: Thread = Thread(target=self._start, daemon=False)
        self.eventLoop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
        self.server: Optional[websockets.server] = None
        self.port: int = port

        self.dataReceivedHandler: List[Callable] = list()

        self.stop: Future = self.eventLoop.create_future()

        self.socketLock = Lock()
        self.connections = dict()

        if autostart:
            self.Start()

        #if waitForStartup:
        #    self.WaitForStartup()

    def WaitForStartup(self, sleepTime: int = 100):
        while not self.eventLoop.is_running():
            asyncio.sleep(sleepTime)

    def Start(self):
        if not self.thread.is_alive():
            self.thread.start()

    def Stop(self):
        self.stop.set_result(True)
        self.stop.done()
        self.thread.join(timeout=0.25)
        self.eventLoop.stop()

        while self.eventLoop.is_running():
            asyncio.sleep(0.1)

        self.eventLoop.close()

    def _start(self):
        self.eventLoop.run_until_complete(self._server())

    def Send(self, data: str, path: str):
        raise Exception("Not Implemented!")
        asyncio.run_coroutine_threadsafe(self._send(data, path), self.eventLoop)

    async def _send(self, data: str, path: str):
        if path in self.connections:
            await self.connections[path].send(data)

    async def _server(self):
        async with websockets.serve(self.DataReceived, "localhost", self.port, loop=self.eventLoop):
            await self.stop

    async def DataReceived(self, websocket, path):

        self.socketLock.acquire()
        if path not in self.connections:
            self.connections[path] = list()

        self.connections[path].append(websocket)
        self.socketLock.release()

        print("New connection at endpoint: " + str(path) + " from: " + str(websocket.local_address))
        try:
            async for message in websocket:
                for callable in self.dataReceivedHandler:
                    response = callable(message, path)

                    if response != None:
                        try:
                            await websocket.send(response)
                        except:
                            print("Error while sending WS Response!")

        except websockets.exceptions.ConnectionClosedError:
            #exception can happen
            pass
        finally:
            self.socketLock.acquire()
            self.connections[path].remove(websocket)
            self.socketLock.release()
            print("Removed connection at endpoint: " + str(path) + " from: " + str(websocket.local_address))
