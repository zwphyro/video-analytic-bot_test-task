import logging
from aiogram import Router, types
from aiogram.enums import ParseMode

from src.services.db_service import DBService
from src.services.llm_service import LLMService

log = logging.getLogger(__name__)
router = Router()


@router.message()
async def handle_user_request(
    message: types.Message, db_service: DBService, llm_service: LLMService
):
    if message.text is None:
        await message.answer("No prompt provided", parse_mode=ParseMode.MARKDOWN_V2)
        return

    try:
        query = await llm_service.generate_sql_query(message.text)
    except Exception as error:
        log.error(f"Failed to generate SQL query: {error}")
        await message.answer(
            "Failed to generate SQL query", parse_mode=ParseMode.MARKDOWN_V2
        )
        raise

    log.info(f"Generated SQL query:\n{query}")

    try:
        result = await db_service.execute(query)

        await message.answer(
            str(result),
            parse_mode=ParseMode.MARKDOWN_V2,
        )

    except Exception as error:
        log.error(f"Failed to execute query: {error}")
        await message.answer(
            "Failed to execute query", parse_mode=ParseMode.MARKDOWN_V2
        )
        raise
