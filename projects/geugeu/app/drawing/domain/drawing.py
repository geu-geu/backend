from dataclasses import dataclass
from datetime import datetime


@dataclass
class Drawing:
    id: str
    post_id: str
    author_id: str
    content: str
    created_at: datetime
    updated_at: datetime
