import asyncio
import logging

import websockets
from orjson import orjson as json

from config import Config
from generator import Generator


class Server:
    config: Config
    generator: Generator

    def __init__(self, config: Config, generator: Generator) -> None:
        self.config = config
        self.generator = generator
        logging.getLogger("websockets").setLevel(logging.WARNING)

    async def websocket_handler(self, websocket, path) -> None:
        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                    input_string = data.get("input", "")

                    if not input_string:
                        await websocket.send(json.dumps({"error": "Invalid input"}))
                    else:
                        output_string = self.generator.generate(input_string)
                        await websocket.send(json.dumps({"output": output_string}))

                except json.JSONDecodeError:
                    await websocket.send(json.dumps({"error": "Invalid JSON"}))

        except websockets.ConnectionClosedError:
            pass
        except Exception as e:
            print(f"Unexpected error: {e}")

    async def run(self) -> None:
        await websockets.serve(
            self.websocket_handler, "localhost", self.config.websocket_port
        )
        print("WebSocket server running at ws://localhost:8765")

        await asyncio.Future()  # run forever
