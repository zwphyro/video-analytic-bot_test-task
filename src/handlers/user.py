import logging
from aiogram import Router, types

from src.services.db_service import DBService
from src.services.llm_service import LLMService

log = logging.getLogger(__name__)
router = Router()


@router.message()
async def handle_user_request(
    message: types.Message, db_service: DBService, llm_service: LLMService
):
    if not message.text:
        return

    query = await llm_service.generate_sql_query(message.text)
    log.info(f"Generated SQL query:\n{query}")

    result = await db_service.execute(query)
    await message.answer(str(result))
