from dataclasses import dataclass
from datetime import datetime


@dataclass
class DrawingComment:
    id: str
    author_id: str
    drawing_id: str
    content: str
    created_at: datetime
    updated_at: datetime
