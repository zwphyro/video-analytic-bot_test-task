from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class DBService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def execute(self, query):
        result = await self.session.execute(text(query))
        return result.scalar_one()
