from openai import AsyncOpenAI

from src.exceptions import LLMException
from src.prompts import SYSTEM_PROMPT


class LLMService:
    def __init__(self, client: AsyncOpenAI):
        self.client = client

    async def generate_sql_query(self, prompt: str):
        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT,
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                temperature=0.0,
            )

            content = response.choices[0].message.content
            if not content:
                raise ValueError("Empty response")

            return content
        except Exception as error:
            raise LLMException(f"Failed to generate SQL query: {error}")
