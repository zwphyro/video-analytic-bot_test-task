from sqlalchemy.ext.asyncio import AsyncSession
from src.db import AsyncSessionLocal
from src.models.video import Video
from src.models.video_snapshot import VideoSnapshot
from src.parser.schemas import VideoListSchema, VideoSchema, VideoSnapshotSchema


async def parse(file_path: str):
    video_list = validate(file_path)

    with AsyncSessionLocal() as session:
        for video in video_list.videos:
            await add_video(video, session)
            for snapshot in video.snapshots:
                await add_snapshot(snapshot, session)


def validate(file_path: str):
    with open(file_path, "r") as file:
        content = file.read()

    return VideoListSchema.model_validate_json(content)


async def add_video(video: VideoSchema, session: AsyncSession):
    new_video = Video(**video.model_dump())
    session.add(new_video)
    await session.commit()


async def add_snapshot(snapshot: VideoSnapshotSchema, session: AsyncSession):
    new_snapshot = VideoSnapshot(**snapshot.model_dump())
    session.add(new_snapshot)
    await session.commit()
