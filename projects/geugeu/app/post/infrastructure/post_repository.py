from typing import final, override

from sqlmodel import Session, select

from app.models import Post as _Post
from app.post.domain.post import Post
from app.post.domain.post_repository import IPostRepository


@final
class PostRepository(IPostRepository):
    @override
    def save(self, session: Session, post: Post) -> Post:
        _post = _Post(
            id=post.id,
            author_id=post.author_id,
            title=post.title,
            content=post.content,
            created_at=post.created_at,
            updated_at=post.updated_at,
        )
        session.add(_post)
        session.commit()
        session.refresh(_post)
        return Post(**_post.model_dump())

    @override
    def find_by_id(self, session: Session, id: str) -> Post | None:
        _post = session.exec(select(_Post).where(_Post.id == id)).first()
        if not _post:
            return None
        return Post(**_post.model_dump())

    @override
    def update(self, session: Session, post: Post) -> Post:
        _post = session.exec(select(_Post).where(_Post.id == post.id)).first()
        if not _post:
            raise ValueError(f"Post with id {post.id} not found")

        _post.title = post.title
        _post.content = post.content
        _post.updated_at = post.updated_at

        session.add(_post)
        session.commit()
        session.refresh(_post)

        return Post(**_post.model_dump())

    @override
    def delete(self, session: Session, id: str) -> None:
        _post = session.exec(select(_Post).where(_Post.id == id)).first()
        if not _post:
            raise ValueError(f"Post with id {id} not found")

        session.delete(_post)
        session.commit()
