from dataclasses import dataclass


@dataclass
class PostImage:
    id: str
    post_id: str
    image_url: str
