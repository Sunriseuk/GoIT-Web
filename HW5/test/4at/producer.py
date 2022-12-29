import asyncio
import websockets
import sys

async def main(message: str):
    url = 'ws://localhost:8000'
    async with websockets.connect(url) as websocket:
        await websocket.send(message)

        

if __name__ == "__main__":
    asyncio.run(main(message=sys.argv[1])) 
    #после запуска нужно дописать аргумент сообщения "python3 consumer.py HELLO!"