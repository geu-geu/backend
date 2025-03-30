from typing import final, override

from sqlmodel import Session

from app.models import PostComment as _PostComment
from app.post.domain.post_comment import PostComment
from app.post.domain.post_comment_repository import IPostCommentRepository


@final
class PostCommentRepository(IPostCommentRepository):
    @override
    def save(self, session: Session, post_comment: PostComment) -> PostComment:
        _post_comment = _PostComment(
            id=post_comment.id,
            author_id=post_comment.author_id,
            post_id=post_comment.post_id,
            content=post_comment.content,
            created_at=post_comment.created_at,
            updated_at=post_comment.updated_at,
        )
        session.add(_post_comment)
        session.commit()
        session.refresh(_post_comment)
        return PostComment(
            id=_post_comment.id,
            author_id=_post_comment.author_id,
            post_id=_post_comment.post_id,
            content=_post_comment.content,
            created_at=_post_comment.created_at,
            updated_at=_post_comment.updated_at,
        )
