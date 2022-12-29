import asyncio
import websockets



async def main():
    url = 'ws://localhost:8000'
    async with websockets.connect(url) as websocket:
        async for message in websocket: #Проверяет, есть ли сообщение
            print(f'{message=}')

        

if __name__ == "__main__":
    asyncio.run(main())