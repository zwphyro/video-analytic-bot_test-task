import logging
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import AsyncSessionLocal
from src.models import Video, VideoSnapshot
from src.parser.schemas import VideoListSchema

log = logging.getLogger(__name__)


class Parser:
    @classmethod
    async def parse(cls, videos_json: str):
        video_list = VideoListSchema.model_validate_json(videos_json)
        log.info(f"Video list with {len(video_list.videos)} videos was validated")

        async with AsyncSessionLocal() as session:
            try:
                log.info("Adding videos and snapshots to database...")
                await cls._add(video_list, session)
                await session.commit()
                log.info("Successfully added videos and snapshots to database")

            except Exception as error:
                log.error(f"Failed to add videos list to database: {error}")
                await session.rollback()
                raise

    @classmethod
    async def _add(cls, video_list: VideoListSchema, session: AsyncSession):
        for video in video_list.videos:
            new_video = Video(
                **video.model_dump(exclude={"snapshots"}),
                snapshots=[
                    VideoSnapshot(**snapshot.model_dump())
                    for snapshot in video.snapshots
                ],
            )
            session.add(new_video)
