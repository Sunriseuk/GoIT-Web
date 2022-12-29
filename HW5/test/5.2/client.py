import asyncio
import websockets


  
async def main(): #шлем запрос на сервер
    url = 'ws://localhost:8000'
    async with websockets.connect(url) as websocket:
        name = input('Your name is: ')
        await websocket.send(name)

        response = await websocket.recv()
        print(f'<<<< {response=}') 




if __name__ == '__main__':
    asyncio.run(main())