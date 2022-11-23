from datetime import datetime

from sqlalchemy import Column, Integer, DateTime

from lab5.database.models import Base


class IntMessage(Base):  # type: ignore
    __tablename__ = 'int_messages'

    time: Column = Column(DateTime(), default=datetime.utcnow, nullable=False, primary_key=True)
    data: Column = Column(Integer, nullable=False)
