from sqlalchemy.ext.asyncio import AsyncSession
from src.db import AsyncSessionLocal
from src.models import Video, VideoSnapshot
from src.parser.schemas import VideoListSchema, VideoSchema, VideoSnapshotSchema


class Parser:
    @classmethod
    async def parse(cls, file_path: str):
        video_list = cls._validate(file_path)

        async with AsyncSessionLocal() as session:
            for video in video_list.videos:
                await cls._add_video(video, session)
                for snapshot in video.snapshots:
                    await cls._add_snapshot(snapshot, session)

    @classmethod
    def _validate(cls, file_path: str):
        with open(file_path, "r") as file:
            content = file.read()

        return VideoListSchema.model_validate_json(content)

    @classmethod
    async def _add_video(cls, video: VideoSchema, session: AsyncSession):
        new_video = Video(**video.model_dump(exclude={"snapshots"}))
        session.add(new_video)
        await session.commit()

    @classmethod
    async def _add_snapshot(cls, snapshot: VideoSnapshotSchema, session: AsyncSession):
        new_snapshot = VideoSnapshot(**snapshot.model_dump())
        session.add(new_snapshot)
        await session.commit()
