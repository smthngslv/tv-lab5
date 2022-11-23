import random
from typing import Optional

from lab5.dataclasses import RandomIntMessage, RandomFloatMessage
from lab5.queue.base import Base


class Producer(Base):
    """
    Produces messages.
    """

    async def produce(self, *, count: Optional[int] = None) -> None:
        """
        WIll product 'count' number of messages. If 'count' is None, then produces messages until stops.
        :param count: Number of messages to produce, if None, then produces messages until stops.
        :return: None
        """
        while count is None or count > 0:
            if count is not None:
                count -= 1

            if random.random() > 0.5:
                message = RandomFloatMessage(data=random.random())  # type: ignore

            else:
                message = RandomIntMessage(data=random.randint(-2147483648, 2147483647))  # type: ignore

            await self._queue.publish(message)
