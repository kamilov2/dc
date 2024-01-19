import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

class AsyncExampleConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        result = await sync_to_async(self.some_async_method)(text_data_json['message'])

        await self.send(text_data=json.dumps({
            'message': result
        }))

    async def some_async_method(self, message):
        await asyncio.sleep(2)
        return f'Processed message: {message}'
