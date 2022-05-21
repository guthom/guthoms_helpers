import unittest
import asyncio
from unittest import TestCase
import time
from guthoms_helpers.data_transmission.WebsocketClient import WebsocketClient
from guthoms_helpers.data_transmission.WebsocketServer import WebsocketServer
from guthoms_helpers.common_helpers.RandomHelper import RandomHelper

class WebSocketTests(TestCase):

    def setUp(self):
        self.receivedData = list()
        self.server = WebsocketServer(8765, autostart=True, waitForStartup=True)
        time.sleep(1)
        self.client = WebsocketClient(8765, endpoint="/test")

    def tearDown(self):
        self.client.Stop()
        self.server.Stop()
        pass

    def DataReceived(self, data, path):
        self.assertEqual(path, "/test")
        self.receivedData.append(data)

    def test_server(self):
        #hook up to my events
        self.server.dataReceivedHandler.append(self.DataReceived)


        sendet = list()

        for i in range(0, 100):
            data = RandomHelper.RandomString(1000)
            sendet.append(data)
            self.client.Send(data)
            time.sleep(0.01)

        time.sleep(0.5)

        self.assertEqual(sendet.__len__(), self.receivedData.__len__())

        for i in range(0, sendet.__len__()):
            self.assertEqual(sendet[i], self.receivedData[i])

        print("Sended and received data is equal!")



