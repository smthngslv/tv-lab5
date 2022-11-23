from sqlalchemy.orm import declarative_base

# Base model.
Base = declarative_base()

# Import actual models.
from lab5.database.models.int_message import IntMessage
from lab5.database.models.float_message import FloatMessage
