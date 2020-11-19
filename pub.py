import asyncio
import websockets
import json


async def pub():
    uri = "ws://localhost:8765/avocado.foo"
    async with websockets.connect(uri) as websocket:
        data = {'action': 'pub', 'data': 'hello world'}
        await websocket.send(json.dumps(data))
        print("Sending: {}".format(data))

asyncio.get_event_loop().run_until_complete(pub())
