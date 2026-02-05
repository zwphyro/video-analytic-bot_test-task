from datetime import datetime
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, declared_attr, mapped_column
from sqlalchemy import func
from re import sub

from src.settings import settings

engine = create_async_engine(settings.db_url)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


text_id = Annotated[str, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[
    datetime, mapped_column(server_default=func.now(), onupdate=datetime.now)
]


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls):
        tmp = sub("(.)([A-Z][a-z]+)", r"\1_\2", cls.__name__)
        return sub("([a-z0-9])([A-Z])", r"\1_\2", tmp).lower() + "s"

    def __repr__(self) -> str:
        parameters = ", ".join(
            f"{key}={value!r}"
            for key, value in self.__dict__.items()
            if not key.startswith("_")
        )
        return f"<{self.__class__.__name__}({parameters})>"
