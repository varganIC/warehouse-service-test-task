import asyncio
import json
from aiokafka import AIOKafkaConsumer
from domain.models import MovementEvent
from usecases.movement_service import register_movement


class Kafka:
    def __init__(self):
        self.consumer = None
        self._task = None

    async def start(self):
        self.consumer = AIOKafkaConsumer(
            'warehouse_movements',
            bootstrap_servers='localhost:9092',
            group_id='warehouse-service-debug',
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            enable_auto_commit=True,
        )
        self._task = asyncio.create_task(self.consume())

    async def consume(self):
        await self.consumer.start()
        try:
            async for msg in self.consumer:
                try:
                    event = MovementEvent(**msg.value['data'])
                    await register_movement(event)
                except Exception as e:
                    print(f"Error processing message: {e}")
        finally:
            await self.consumer.stop()

    async def stop(self):
        if self.consumer:
            await self.consumer.stop()
        if self._task:
            self._task.cancel()


kafka = Kafka()


async def start_kafka_consumer():
    await kafka.start()


async def kafka_stop_consume():
    await kafka.stop()