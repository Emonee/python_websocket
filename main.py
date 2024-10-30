import asyncio
import websockets

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
    async with websockets.serve(echo, "localhost", 5000):
        print("WebSocket server is running on ws://localhost:8765")
        await asyncio.Future()  # Run forever

# Start the asyncio event loop
if __name__ == "__main__":
    asyncio.run(main())
