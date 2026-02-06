from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db import Base, text_id, created_at, updated_at


class Video(Base):
    id: Mapped[text_id]

    video_created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    views_count: Mapped[int]
    likes_count: Mapped[int]
    reports_count: Mapped[int]
    comments_count: Mapped[int]
    creator_id: Mapped[str]

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    snapshots: Mapped[list["VideoSnapshot"]] = relationship(back_populates="video")  # type: ignore[no-undefined-variable] # NOQA: F821
