#!/bin/env python3

import asyncio
import json
import websockets


class LocalComponent:
    """We could have a local commponet for faster connection.

    This component could use an UNIX socket or other communication method
    different from websocket, if needed.

    But, for consistency we should provide the same API (
    """
    def start(self):
        raise NotImplementedError

    def publish(self, topic, data):
        raise NotImplementedError


class RemoteComponent:
    def __init__(self):
        # This should be a config option
        self.url = "ws://localhost:8765"
        self.subscribers = {}
        self.loop = asyncio.get_event_loop()

        # Populating subscribers with local methods and topics
        for method in self._get_decorated_methods():
            try:
                self.subscribers[method.topic].add(method)
            except KeyError:
                self.subscribers[method.topic] = {method}

    async def _connect_to_topic(self, topic):
        endpoint = "{}/{}".format(self.url, topic)
        async with websockets.connect(endpoint) as websocket:
            data = {'action': 'sub'}
            await websocket.send(json.dumps(data))
            print("Sending: {}".format(data))

            # Wait for events on that topic
            async for data in websocket:
                message = json.loads(data)
                if not self._is_pub_on_topic(message, topic):
                    continue

                # Call all subscribers with data
                for method in self.subscribers.get(topic):
                    method(message.get('data'))

    def _is_pub_on_topic(self, message, topic):
        if message.get('action') != 'pub':
            return False
        if message.get('topic') != "/{}".format(topic):
            return False
        return True

    def _get_decorated_methods(self):
        return [getattr(self, method_name) for method_name in
                dir(self) if method_name[0] != '_' and
                callable(getattr(self, method_name)) and
                hasattr(getattr(self, method_name), 'topic')]

    async def start(self):
        # For each topic triggering one connection to the server
        for topic in self.subscribers:
            print("Subscribing to {}".format(topic))
            await self._connect_to_topic(topic)

    def publish(self, topic, data):
        async def pub(topic, data):
            endpoint = "{}/{}".format(self.url, topic)
            async with websockets.connect(endpoint) as websocket:
                data = {'action': 'pub', 'data': data}
                print("Sending: {}".format(data))
                await websocket.send(json.dumps(data))
        asyncio.ensure_future(pub(topic, data))
