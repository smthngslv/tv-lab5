from typing import AsyncGenerator

import aio_pika
from aio_pika import RobustConnection, RobustChannel, RobustQueue, Message as AioPikaMessage

from lab5.dataclasses import Message


class RabbitMQQueue:
    """
    This is the class that represents queue in RabbitMQ. It can publish and consume messages.
    """

    def __init__(self, amqp_url: str, queue_name: str) -> None:
        """
        This is the class that represents queue in RabbitMQ. It can publish and consume messages.

        :param amqp_url: The URL to the rabbitmq in the format of amqp://user:password@host:port.
        :param queue_name: Name of the queue, that will be used.
        """
        self.__amqp_url = amqp_url
        self.__queue_name = queue_name

        # This will be initialized when we connect.
        self.__connection: RobustConnection | None = None
        self.__channel: RobustChannel | None = None
        self.__queue: RobustQueue | None = None

    @property
    def is_connected(self) -> bool:
        """
        :return: True if we are connected to the RabbitMQ, False otherwise.
        """
        return self.__connection is not None and not self.__connection.is_closed

    async def connect(self) -> None:
        """
        Connects to the RabbitMQ.
        :return: None
        """
        if self.is_connected:
            raise ValueError('Already connected.')

        # Connect to RabbitMQ.
        self.__connection = await aio_pika.connect_robust(self.__amqp_url)  # type: ignore
        # Create a channel. This is a communication channel inside TCP connection.
        self.__channel = await self.__connection.channel()  # type: ignore
        # Declare a queue. If queue already exists, this method does nothing.
        self.__queue = await self.__channel.declare_queue(self.__queue_name)  # type: ignore

    async def disconnect(self) -> None:
        """
        Disconnects from the RabbitMQ.
        :return: None
        """
        if not self.is_connected:
            raise ValueError('Already disconnected.')

        # Close connection and channel.
        await self.__channel.close()  # type: ignore
        await self.__connection.close()  # type: ignore

        self.__queue = None
        self.__channel = None
        self.__connection = None

    async def publish(self, message: Message) -> None:
        """
        Sends the message into the queue.
        :param message: Message to send.
        :return: None
        """
        if not self.is_connected:
            raise ValueError('Not connected.')

        # Serialize message with msgpack and send it via default exchange with routing key equals to target queue name.
        await self.__channel.default_exchange.publish(  # type: ignore
            AioPikaMessage(message.msgpack()), routing_key=self.__queue_name
        )

    async def consume(self) -> AsyncGenerator[Message, None]:
        """
        Consumes messages from the queue.
        :return: None
        """
        if not self.is_connected:
            raise ValueError('Not connected.')

        # Create queue iterator.
        async with self.__queue.iterator() as iterator:  # type: ignore
            # Iterate over messages.
            async for message in iterator:
                async with message.process():  # type: ignore
                    yield Message.parse_msgpack(message.body)  # type: ignore

    async def __aenter__(self) -> 'RabbitMQQueue':
        """
        Allows use this class in context manager
        :return: RabbitMQQueue
        """
        await self.connect()
        return self

    async def __aexit__(self, *_) -> None:
        """
        Allows use this class in context manager
        :return: None
        """
        await self.disconnect()
