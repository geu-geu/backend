from typing import final, override

from sqlmodel import Session, select

from app.database import engine
from app.models import Post as _Post
from app.post.domain.post import Post
from app.post.domain.post_repository import IPostRepository


@final
class PostRepository(IPostRepository):
    @override
    def save(self, post: Post) -> Post:
        _post = _Post(
            id=post.id,
            author_id=post.author_id,
            title=post.title,
            content=post.content,
            created_at=post.created_at,
            updated_at=post.updated_at,
        )
        with Session(engine) as session:
            session.add(_post)
            session.commit()
            session.refresh(_post)
        return Post(**_post.model_dump())

    @override
    def find_by_id(self, id: str) -> Post | None:
        with Session(engine) as session:
            _post = session.exec(select(_Post).where(_Post.id == id)).first()
        if not _post:
            return None
        return Post(**_post.model_dump())
