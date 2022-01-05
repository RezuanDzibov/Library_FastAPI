import uuid

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID


class UUIDMixin:
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
