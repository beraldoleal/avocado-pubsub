#!/bin/env python3
"""Basic PUB/SUB broker.

This is a standalone script but if incorporated should be started together with
avocado, internally.
"""

import asyncio
import json
import websockets


def log(msg, level="INFO"):
    print("{}: {}".format(level.upper(), msg))


class AvocadoBroker:
    def __init__(self, host='127.0.0.1', port='9999'):
        self.host = host
        self.port = port

        self.subscribers = {}

    async def remove_client(self, client):
        for topic in self.subscribers:
            self.subscribers[topic].remove(client)

    async def handle_new_message(self, websocket, topic):
        try:
            async for data in websocket:
                message = json.loads(data)
                action = message.get('action')
                if action == 'sub':
                    await self.subscribe(topic, websocket)
                elif action == 'pub':
                    await self.publish(topic, message.get('data'))
                else:
                    log("Not supported action: {}".format(action))
        except websockets.exceptions.ConnectionClosedError:
            log("Connection closed from {}".format(websocket))
            await self.remove_client(websocket)

    async def subscribe(self, topic, client):
        log("{} subscribed to {}".format(client.remote_address[0],
                                         topic))
        try:
            self.subscribers[topic].add(client)
        except KeyError:
            self.subscribers[topic] = {client}

    async def publish(self, topic, data):
        log("{} published on {}".format(data, topic))

        subscribers = self.subscribers.get(topic, {})
        log("Sending to {} clients.".format(len(subscribers)))
        for client in subscribers:
            await client.send(json.dumps({'action': 'pub',
                                          'topic': topic,
                                          'data': data}))

    def wait_closed(self):
        pass


if __name__ == "__main__":
    host, port = "localhost", "8765"
    broker = AvocadoBroker()
    loop = asyncio.get_event_loop()

    log("Starting broker at {}:{}".format(host, port))
    server = websockets.serve(broker.handle_new_message, host, port)
    loop.run_until_complete(server)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        log("Stopping server...")
        loop.run_until_complete(broker.wait_closed())
        loop.close()
