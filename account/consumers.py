from channels.generic.websocket import AsyncJsonWebsocketConsumer
import asyncio

class EchoConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_id = "echo_1"

        await self.channel_layer.group_add(
            self.room_id,
            self.channel_name
        )
        await self.accept()

        while True:
            await asyncio.ensure_future(self.periodMessage())

    async def periodMessage(self):
        await self.send('hello!')
        await asyncio.sleep(1)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_id,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            await self.channel_layer.group_send(
                self.room_id,
                {
                    'type': 'echo_message',
                    'message': text_data + " - Sent By Server"
                }
            )

    async def echo_message(self, event):
        message = event['message']
        await self.send_json(event)