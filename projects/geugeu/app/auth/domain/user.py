from dataclasses import dataclass


@dataclass
class User:
    id: str
    email: str
    password: str
    is_active: bool
    is_admin: bool
