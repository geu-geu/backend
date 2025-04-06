from typing import final, override

from sqlmodel import Session, select

from app.drawing.domain.post import Post
from app.drawing.repositories.post_repository import IPostRepository
from app.models import Post as _Post


@final
class PostRepositoryImpl(IPostRepository):
    @override
    def find_by_id(self, session: Session, id: str) -> Post | None:
        post = session.exec(select(_Post).where(_Post.id == id)).first()
        return Post(id=post.id) if post else None
