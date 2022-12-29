#server - соодиняет отправителя и получателя
#consumer - получает сообщения
#producer - отправлет сообщения
import asyncio
from h11 import ConnectionClosed
import websockets
from websockets.legacy.server import WebSocketServerProtocol
from faker import Faker

fake = Faker()

class Server:
    clients: set [WebSocketServerProtocol] = set()

    async def register(self, ws: WebSocketServerProtocol):
        ws.name = fake.name()

        self.clients.add(ws)
        print(f'Connection established {ws.remote_address=}') 

    async def unregister(self, ws: WebSocketServerProtocol):
        self.client.remove(ws)
        print(f'Connection disconnected {ws.remote_address=}') 

    #Отправка сообщения
    async def send_to_client(self, message: str):
        if self.clients:
            for client in self.clients:
                await client.send(message)

    async def ws_handler(self, websocket: WebSocketServerProtocol):
        print(f'{websocket=}')
        await self.register(websocket) #регистрация
        try:
            async for message in websocket: #проверка сообщения
                print(f'{message}')
                await self.send_to_client(message)
        except ConnectionClosedOk:
            pass 


async def main(): #Запускаем сервер
    server = Server() #создаем экземпляр класса сервер
    async with websockets.serve(server.ws_handler, 'localhost', 8000): 
        await asyncio.Future() #Работает постоянно


if __name__ == '__main__':
    asyncio.run(main())    