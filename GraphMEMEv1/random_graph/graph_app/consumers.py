# graph_app/consumers.py
import json
import asyncio
import random
from channels.generic.websocket import AsyncWebsocketConsumer


class GraphConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'graph_data'

        # Присоединяемся к группе
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Разрешаем соединение
        await self.accept()

        # Начинаем отправлять данные каждую секунду
        while True:
            data = {
                'value': random.uniform(-1, 1),  # случайное значение для графика
            }
            await self.send(text_data=json.dumps(data))  # отправляем данные в WebSocket

            await asyncio.sleep(1)  # задержка в 1 секунду перед отправкой следующего значения

    async def disconnect(self, close_code):
        # Отключаемся от группы
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
