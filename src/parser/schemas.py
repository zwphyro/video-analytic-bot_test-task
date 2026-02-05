from datetime import datetime
from pydantic import BaseModel


class VideoSnapshotSchema(BaseModel):
    id: str
    video_id: str

    views_count: int
    likes_count: int
    reports_count: int
    comments_count: int

    delta_views_count: int
    delta_likes_count: int
    delta_reports_count: int
    delta_comments_count: int

    created_at: datetime
    updated_at: datetime


class VideoSchema(BaseModel):
    id: str
    video_created_at: datetime

    views_count: int
    likes_count: int
    reports_count: int
    comments_count: int

    creator_id: str

    created_at: datetime
    updated_at: datetime

    snapshots: list[VideoSnapshotSchema]


class VideoListSchema(BaseModel):
    videos: list[VideoSchema]
