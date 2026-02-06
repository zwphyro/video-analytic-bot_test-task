import logging
from typing import Awaitable, Callable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.services.db_service import DBService

log = logging.getLogger(__name__)


class DBMiddleware(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        super().__init__()
        self.session_pool = session_pool

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, any]], Awaitable[any]],
        event: TelegramObject,
        data: dict[str, any],
    ):
        async with self.session_pool() as session:
            db_service = DBService(session)
            data["db_service"] = db_service
            try:
                result = await handler(event, data)
                await session.commit()
                return result
            except Exception as error:
                log.error(f"Failed to execute handler: {error}")
                await session.rollback()
                raise
