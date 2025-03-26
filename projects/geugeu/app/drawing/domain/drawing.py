from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class DrawingStatus(StrEnum):
    DRAFT = "DRAFT"  # 그릴게요 버튼으로 생성된 초기 상태
    COMPLETED = "COMPLETED"  # 그림이 완성된 상태


@dataclass
class Drawing:
    id: str
    post_id: str
    author_id: str
    content: str
    status: DrawingStatus
    created_at: datetime
    updated_at: datetime
