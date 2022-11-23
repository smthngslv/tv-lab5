from lab5.database import DatabaseEngine
from lab5.database.models import IntMessage, FloatMessage
from lab5.dataclasses import RandomIntMessage, RandomFloatMessage
from lab5.queue.base import Base
from lab5.settings import settings


class Consumer(Base):
    """
    Consumes messages.
    """

    def __init__(self) -> None:
        """
        Consumes messages.
        """
        # Initialize parent class.
        super().__init__()

        # Connection to PostgreSQL.
        self.__database = DatabaseEngine(settings.DATABASE_URL)

    async def consume(self) -> None:
        """
        Consumes messages from the queue.
        :return: None
        """
        # Get session for the PostgreSQL.
        async with self.__database.get_session() as session:
            # Iterate over messages.
            async for message in self._queue.consume():
                match message:
                    case RandomIntMessage():
                        model = IntMessage(data=message.data)

                    case RandomFloatMessage():
                        model = FloatMessage(data=message.data)

                    case _:
                        raise ValueError(f'Unknown message: {message}.')

                # Add message to the PostgreSQL.
                session.add(model)
                await session.commit()

    async def disconnect(self) -> None:
        """
        Disconnects from the queue.
        :return: None
        """
        await super().disconnect()
        await self.__database.disconnect()
