from datetime import datetime

from sqlalchemy import Column, Float, DateTime

from lab5.database.models import Base


class FloatMessage(Base):
    __tablename__ = 'float_messages'

    time: Column = Column(DateTime(), default=datetime.utcnow, nullable=False, primary_key=True)
    data: Column = Column(Float, nullable=False)
