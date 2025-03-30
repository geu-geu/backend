from dataclasses import dataclass
from datetime import datetime

from sqlmodel import SQLModel


@dataclass
class PostComment(SQLModel):
    id: str
    author_id: str
    post_id: str
    content: str
    created_at: datetime
    updated_at: datetime
