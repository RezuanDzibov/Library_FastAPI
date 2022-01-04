import uuid

from sqlalchemy import Column
import sqlalchemy_utils as sau


class UUIDMixin:
    id = Column(sau.UUIDType(binary=False), primary_key=True, default=uuid.uuid4)