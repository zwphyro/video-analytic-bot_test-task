from argparse import ArgumentParser
import asyncio
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from openai import AsyncOpenAI

from src.handlers.errors import register_error_handlers
from src.handlers.user import router
from src.db import AsyncSessionLocal
from src.middlewares.db_middleware import DBMiddleware
from src.middlewares.llm_middleware import LLMMiddleware
from src.parser import Parser
from src.settings import settings
from src.logging import configure_logging

configure_logging(settings.log_level)


async def main():
    argument_parser = ArgumentParser()
    argument_parser.add_argument("--parse", action="store_true")
    args = argument_parser.parse_args()
    if args.parse:
        videos_json = sys.stdin.read()
        await Parser.parse(videos_json)
        return

    client = AsyncOpenAI(
        base_url=settings.openai_base_url, api_key=settings.openai_api_key
    )

    bot = Bot(
        token=settings.tg_bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2),
    )

    dispatcher = Dispatcher()
    dispatcher.update.middleware(DBMiddleware(AsyncSessionLocal))
    dispatcher.update.middleware(LLMMiddleware(client))
    dispatcher.include_router(router)

    register_error_handlers(router)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dispatcher.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
