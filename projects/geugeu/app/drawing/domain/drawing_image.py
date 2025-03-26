from dataclasses import dataclass


@dataclass
class DrawingImage:
    id: str
    drawing_id: str
    image_url: str
