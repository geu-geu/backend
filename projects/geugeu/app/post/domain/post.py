from dataclasses import dataclass
from datetime import datetime


@dataclass
class Post:
    id: str
    author_id: str
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
