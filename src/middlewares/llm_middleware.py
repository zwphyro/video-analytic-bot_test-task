from typing import Awaitable, Callable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from openai import AsyncOpenAI

from src.services.llm_service import LLMService


class LLMMiddleware(BaseMiddleware):
    def __init__(self, client: AsyncOpenAI):
        super().__init__()
        self.client = client

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, any]], Awaitable[any]],
        event: TelegramObject,
        data: dict[str, any],
    ):
        llm_service = LLMService(self.client)
        data["llm_service"] = llm_service
        return await handler(event, data)
