import asyncio
import websockets
from websockets.legacy.server import WebSocketServerProtocol


async def ws_hamdler(websocket: WebSocketServerProtocol):
    print(f'{websocket=}')
     

async def main(): #Запускаем сервер
    async with websockets.server.serve(ws_hamdler, 'localhost', 8000): 
        await asyncio.Future() #Работает постоянно



if __name__ == '__main__':
    asyncio.run(main())