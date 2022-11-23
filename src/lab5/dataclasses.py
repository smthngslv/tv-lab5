from enum import Enum
from functools import partial
from typing import Literal, Annotated, Type, TypeVar

import msgpack
from pydantic import BaseModel, Field, parse_obj_as, parse_raw_as

# Generic variable. I use it to annotate the code.
T = TypeVar(name='T', bound=BaseModel)  # type: ignore


class MessageType(int, Enum):
    """
    This is enum, that indicates type of message.
    """

    RANDOM_INT = 0
    RANDOM_FLOAT = 1


class MessageBase(BaseModel):
    """
    This is base class for message. Any message should contain type. With this type we can determine type of message.
    """

    type: MessageType

    def msgpack(self) -> bytes:
        """
        Serialize message into bytes, using msgpack.
        :return: Serialized message in bytes.
        """
        return msgpack.packb(self.dict(exclude_none=True))

    @classmethod
    def parse_msgpack(cls: Type[T], data: bytes) -> T:  # type: ignore
        """
        Deserialize message from bytes, using msgpack.
        :param data: Serialized message in bytes.
        :return: Deserialized message.
        """
        return cls.parse_obj(msgpack.unpackb(data))  # type: ignore


class RandomIntMessage(MessageBase):
    """
    This message contains random integer, and has corresponding type.
    """

    # The type cannot change, so make it literal with default value.
    type: Literal[MessageType.RANDOM_INT] = MessageType.RANDOM_INT

    # This is actually data
    data: int = Field(description='Random integer.')


class RandomFloatMessage(MessageBase):
    """
    This message contains random float, and has corresponding type.
    """

    # The type cannot change, so make it literal with default value.
    type: Literal[MessageType.RANDOM_FLOAT] = MessageType.RANDOM_FLOAT

    # This is actually data
    data: float = Field(description='Random float.')


# This will create a compound type from two types - RandomIntMessage and RandomFloatMessage. As I described above,
# the field 'type' is used to determine the actual type of the message, therefore it is discriminator of these types.
Message = Annotated[RandomIntMessage | RandomFloatMessage, Field(discriminator='type')]

# This is little dirty, but very useful hack. This three lines add three methods to the compound type 'Message'.
# First method - 'parse_obj' will try to parse any dict into RandomIntMessage or RandomFloatMessage.
# Since, we make 'type' field as discriminator, the pydantic will first parse this field, and then pick the correct
# type (RandomIntMessage or RandomFloatMessage) to parse rest of the message.
Message.__dict__['parse_obj'] = partial(parse_obj_as, Message)
# Second method - 'parse_raw' does same, but for any JSON string.
Message.__dict__['parse_raw'] = partial(parse_raw_as, Message)
# Third method - 'parse_msgpack' does same, but for any msgpacked bytes.
Message.__dict__['parse_msgpack'] = lambda raw: Message.parse_obj(msgpack.unpackb(raw))  # type: ignore
# Now, we can use Message as any other pydantic model. We can use Message.parse_msgpack(b'our serialized message') and
# pydantic will automatically decode it from msgpack, determine the type, use right model to validate the data and
# return instance of RandomIntMessage or RandomFloatMessage class, depending on type.
