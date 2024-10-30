import asyncio
import websockets
import os

port = int(os.getenv("PORT", 5000))

def health_check(connection, request):
    if request.path == "/healthz":
        return connection.respond(HTTPStatus.OK, "OK")

# Define the handler for new WebSocket connections
async def echo(websocket, path):
    print("New connection established")
    try:
        async for message in websocket:
            print(f"Received message: {message}")
            await websocket.send(f"Echo: {message}")
    except websockets.ConnectionClosedOK:
        print("Connection closed")

# Run the WebSocket server on localhost at port 8765
async def main():
    async with websockets.serve(echo, "0.0.0.0", port, process_request=health_check):
        print(f"WebSocket server is running on ws://0.0.0.0:{port}")
        await asyncio.Future()  # Run forever

# Start the asyncio event loop
if __name__ == "__main__":
    asyncio.run(main())
