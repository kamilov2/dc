# main/consumers.py
import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Profile
from .serializers import AsyncProfileSerializer

class AsyncExampleConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('async_example_group', self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type')

        if message_type == 'start':
            await self.start_streaming()
        elif message_type == 'stop':
            await self.stop_streaming()

    async def start_streaming(self):
        profiles = await database_sync_to_async(Profile.objects.filter(permission=True).only('name', 'device_id', 'permission').defer('created_at', 'updated_at')[:15])()
        for profile in profiles:
            serialized_profile = await database_sync_to_async(AsyncProfileSerializer(profile).data)()
            await self.send(text_data=json.dumps({
                'type': 'stream',
                'data': serialized_profile,
            }))

            await asyncio.sleep(0.1)

    async def stop_streaming(self):
        await self.send(text_data=json.dumps({
            'type': 'stream',
            'data': 'Streaming stopped',
        }))
