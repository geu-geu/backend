from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    id: str
    email: str
    name: str | None
    password: str
    is_admin: bool
    is_active: bool
    is_verified: bool
    profile_image_url: str | None
    created_at: datetime
    updated_at: datetime
