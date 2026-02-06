from argparse import ArgumentParser
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from src.bot.routes import router
from src.db import AsyncSessionLocal
from src.middleware import DBMiddleware
from src.parser import Parser
from src.settings import settings
from src.logging import configure_logging

configure_logging(settings.log_level)


async def main():
    argument_parser = ArgumentParser()
    argument_parser.add_argument("--parse", type=str)
    args = argument_parser.parse_args()
    if args.parse:
        await Parser.parse(args.parse)
        return

    bot = Bot(
        token=settings.tg_bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2),
    )

    dispatcher = Dispatcher()
    dispatcher.update.middleware(DBMiddleware(AsyncSessionLocal))
    dispatcher.include_router(router)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dispatcher.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
