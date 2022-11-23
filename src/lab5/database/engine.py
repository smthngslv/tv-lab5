from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


class DatabaseEngine:
    """
    This is connector for PostgreSQL.
    """

    def __init__(self, url: str) -> None:
        """
        This is connector for PostgreSQL.
        :param url: The URL to the postgres in the format of postgres://user:password@host:port.
        """
        # Create async db engine. Flag 'future=True' means that we use new 2.0 API.
        self.__db_engine = create_async_engine(url, future=True)
        # Create session maker. It will generate new sessions on the demand.
        self.__db_session_maker = sessionmaker(
            self.__db_engine, expire_on_commit=False, class_=AsyncSession, future=True
        )

    def get_session(self) -> AsyncSession:
        """
        Starts new sessions.
        :return: AsyncSession.
        """
        return self.__db_session_maker()

    async def disconnect(self) -> None:
        """
        Disconnects from postgres.
        :return: None
        """
        await self.__db_engine.dispose()
