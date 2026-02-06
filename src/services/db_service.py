from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import DBException


class DBService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def execute(self, query):
        try:
            result = await self.session.execute(text(query))
            return result.scalar_one()
        except Exception as e:
            raise DBException(f"Failed to execute query: {e}")
