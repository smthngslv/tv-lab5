from abc import ABC
from typing import TypeVar

from lab5.settings import settings
from lab5.utils.rabbitmq_queue import RabbitMQQueue

# Generic variable. I use it to annotate the code.
T = TypeVar(name='T')  # type: ignore


class Base(ABC):
    """
    Base class for the consumer and producer.
    """

    def __init__(self) -> None:
        """
        Base class for the consumer and producer.
        """
        self._queue = RabbitMQQueue(settings.AMQP_URL, settings.AMQP_QUEUE)

    async def connect(self) -> None:
        """
        Connects to the queue.
        :return: None
        """
        await self._queue.connect()

    async def disconnect(self) -> None:
        """
        Disconnects from the queue.
        :return: None
        """
        await self._queue.disconnect()

    async def __aenter__(self: T) -> 'T':  # type: ignore
        """
        Allows use this class in context manager
        :return: Self.
        """
        await self._queue.connect()  # type: ignore
        return self

    async def __aexit__(self, *_) -> None:
        """
        Allows use this class in context manager
        :return: None
        """
        await self._queue.disconnect()
