import asyncio
import json

import websockets


async def websocket_client(uri: str):
    async with websockets.connect(uri) as websocket:
        while True:
            # Prompt for user input
            input_string = input(
                "Enter a string to send to the server (or 'quit' to exit): "
            )
            if input_string.lower() == "quit":
                break

            # Send a JSON object containing a key "input" with the input string
            message = json.dumps({"input": input_string})
            await websocket.send(message)

            # Receive and print the server response
            response = await websocket.recv()
            response_data = json.loads(response)
            print("Response: " + response_data["output"])


if __name__ == "__main__":
    uri = "ws://localhost:8765"
    asyncio.get_event_loop().run_until_complete(websocket_client(uri))
