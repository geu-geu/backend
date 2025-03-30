from abc import ABC, abstractmethod

from sqlmodel import Session

from app.post.domain.post_comment import PostComment


class IPostCommentRepository(ABC):
    @abstractmethod
    def save(self, session: Session, post_comment: PostComment) -> PostComment:
        raise NotImplementedError

    @abstractmethod
    def find_all_by_post_id(self, session: Session, post_id: str) -> list[PostComment]:
        raise NotImplementedError
