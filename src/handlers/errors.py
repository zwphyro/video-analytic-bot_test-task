import logging
from aiogram import Router
from aiogram.types import ErrorEvent
from src.exceptions import LLMException, DBException

log = logging.getLogger(__name__)


async def handle_llm_exception(event: ErrorEvent):
    log.error(f": {event.exception}", exc_info=True)
    if event.update.message:
        await event.update.message.answer("Failed to generate SQL query")


async def handle_db_exception(event: ErrorEvent):
    log.error(f": {event.exception}", exc_info=True)
    if event.update.message:
        await event.update.message.answer("Failed to execute query")


async def handle_unknown_exception(event: ErrorEvent):
    log.critical(f"Unknown exception: {event.exception}", exc_info=True)
    if event.update.message:
        await event.update.message.answer("Internal server error")


def register_error_handlers(router: Router):
    router.error.register(
        handle_llm_exception, lambda e: isinstance(e.exception, LLMException)
    )
    router.error.register(
        handle_db_exception, lambda e: isinstance(e.exception, DBException)
    )
    router.error.register(handle_unknown_exception)
