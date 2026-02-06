import logging
from aiogram import Router, types
from aiogram.enums import ParseMode

from src.services.db_service import DBService

log = logging.getLogger(__name__)
router = Router()


@router.message()
async def handle_user_request(message: types.Message, db_service: DBService):
    query = "SELECT COALESCE(SUM(delta_likes_count), 0) FROM video_snapshots WHERE created_at >= '2025-05-01 00:00:00+00' AND created_at <= '2025-05-01 23:59:59+00';"
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
