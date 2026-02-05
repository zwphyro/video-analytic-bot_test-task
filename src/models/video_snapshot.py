from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db import Base, text_id, created_at, updated_at


class VideoSnapshot(Base):
    id: Mapped[text_id]

    video_id: Mapped[text_id] = mapped_column(ForeignKey("videos.id"))
    views_count: Mapped[int]
    likes_count: Mapped[int]
    reports_count: Mapped[int]
    comments_count: Mapped[int]

    delta_views_count: Mapped[int]
    delta_likes_count: Mapped[int]
    delta_reports_count: Mapped[int]
    delta_comments_count: Mapped[int]

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    video: Mapped["Video"] = relationship(back_populates="snapshots")
