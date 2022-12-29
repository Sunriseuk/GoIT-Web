import asyncio
import websockets
from websockets.legacy.server import WebSocketServerProtocol


async def ws_handler(websocket: WebSocketServerProtocol):
    print(f'{websocket=}') #Когда будет устанавливаться соединение, об этом будет ссобщать принт
    request = await websocket.recv()
    print(f'{request=}')
    await websocket.send(f'Hello {request}')

async def main(): #Запускаем сервер
    async with websockets.serve(ws_handler, 'localhost', 8000): 
        await asyncio.Future() #Работает постоянно



if __name__ == '__main__':
    asyncio.run(main())