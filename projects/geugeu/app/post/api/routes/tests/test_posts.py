from datetime import UTC, datetime

from fastapi.testclient import TestClient
from sqlmodel import Session
from ulid import ULID

from app.auth.domain.user import User
from app.main import app
from app.post.domain.post import Post
from app.post.domain.post_comment import PostComment
from app.post.repositories.post_comment_repository import IPostCommentRepository
from app.post.repositories.post_repository import IPostRepository

client = TestClient(app)


def test_create_post():
    # given
    title = "title"
    content = "content"
    image_urls = [
        "https://example.com/image1.png",
        "https://example.com/image2.png",
    ]

    # when
    response = client.post(
        "/api/posts",
        json={"title": title, "content": content, "image_urls": image_urls},
    )

    # then
    assert response.status_code == 201
    assert response.json()["title"] == title
    assert response.json()["content"] == content
    assert response.json()["images"] == image_urls


def test_get_post(post_repository: IPostRepository, session: Session):
    # given
    post = Post(
        id=str(ULID()),
        author_id=str(ULID()),
        title="title",
        content="content",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    post_repository.save(session, post)

    # when
    response = client.get(f"/api/posts/{post.id}")

    # then
    assert response.status_code == 200
    assert response.json()["id"] == post.id
    assert response.json()["title"] == post.title
    assert response.json()["content"] == post.content


def test_update_post(session: Session, post_repository: IPostRepository):
    # given
    post = Post(
        id=str(ULID()),
        author_id=str(ULID()),
        title="title",
        content="content",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    post_repository.save(session, post)

    updated_title = "updated title"
    updated_content = "updated content"
    updated_image_urls = [
        "https://example.com/updated_image1.png",
        "https://example.com/updated_image2.png",
    ]

    # when
    response = client.put(
        f"/api/posts/{post.id}",
        json={
            "title": updated_title,
            "content": updated_content,
            "image_urls": updated_image_urls,
        },
    )

    # then
    assert response.status_code == 200
    assert response.json()["id"] == post.id
    assert response.json()["title"] == updated_title
    assert response.json()["content"] == updated_content
    assert response.json()["images"] == updated_image_urls


def test_delete_post(session: Session, post_repository: IPostRepository):
    # given
    post = Post(
        id=str(ULID()),
        author_id=str(ULID()),
        title="title",
        content="content",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    post_repository.save(session, post)
    assert post_repository.find_by_id(session, post.id) is not None

    # when
    response = client.delete(f"/api/posts/{post.id}")

    # then
    assert response.status_code == 204
    assert post_repository.find_by_id(session, post.id) is None


def test_create_post_comment(
    session: Session,
    post_repository: IPostRepository,
    user: User,
):
    # given
    post = Post(
        id=str(ULID()),
        author_id=str(ULID()),
        title="title",
        content="content",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    post_repository.save(session, post)

    # when
    response = client.post(
        f"/api/posts/{post.id}/comments",
        json={"content": "comment"},
    )

    # then
    assert response.status_code == 201
    assert response.json()["id"] is not None
    assert response.json()["author_id"] == user.id
    assert response.json()["post_id"] == post.id
    assert response.json()["content"] == "comment"


def test_get_post_comments(
    session: Session,
    post_repository: IPostRepository,
    post_comment_repository: IPostCommentRepository,
):
    # given
    post = Post(
        id=str(ULID()),
        author_id=str(ULID()),
        title="title",
        content="content",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    post_repository.save(session, post)

    post_comment = PostComment(
        id=str(ULID()),
        author_id=str(ULID()),
        post_id=post.id,
        content="comment",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    post_comment_repository.save(session, post_comment)

    # when
    response = client.get(f"/api/posts/{post.id}/comments")

    # then
    assert response.status_code == 200
    assert response.json()[0]["id"] == post_comment.id
    assert response.json()[0]["author_id"] == post_comment.author_id
    assert response.json()[0]["post_id"] == post_comment.post_id
    assert response.json()[0]["content"] == post_comment.content


def test_update_post_comment(
    session: Session,
    post_repository: IPostRepository,
    post_comment_repository: IPostCommentRepository,
    user: User,
):
    # given
    post = Post(
        id=str(ULID()),
        author_id=str(ULID()),
        title="title",
        content="content",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    post_repository.save(session, post)

    post_comment = PostComment(
        id=str(ULID()),
        author_id=user.id,
        post_id=post.id,
        content="original comment",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    post_comment_repository.save(session, post_comment)

    # when
    response = client.put(
        f"/api/posts/{post.id}/comments/{post_comment.id}",
        json={"content": "updated comment"},
    )

    # then
    assert response.status_code == 200
    assert response.json()["id"] == post_comment.id
    assert response.json()["author_id"] == post_comment.author_id
    assert response.json()["post_id"] == post_comment.post_id
    assert response.json()["content"] == "updated comment"


def test_update_post_comment_with_unauthorized_user(
    session: Session,
    post_repository: IPostRepository,
    post_comment_repository: IPostCommentRepository,
    user: User,
):
    # given
    post = Post(
        id=str(ULID()),
        author_id=str(ULID()),
        title="title",
        content="content",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    post_repository.save(session, post)

    post_comment = PostComment(
        id=str(ULID()),
        author_id=str(ULID()),  # different user
        post_id=post.id,
        content="comment",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    post_comment_repository.save(session, post_comment)

    # when
    response = client.put(
        f"/api/posts/{post.id}/comments/{post_comment.id}",
        json={"content": "updated comment"},
    )

    # then
    assert response.status_code == 403
    assert response.json()["detail"] == "You are not the author of this comment"


def test_delete_post_comment(
    session: Session,
    post_repository: IPostRepository,
    post_comment_repository: IPostCommentRepository,
    user: User,
):
    # given
    post = Post(
        id=str(ULID()),
        author_id=str(ULID()),
        title="title",
        content="content",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    post_repository.save(session, post)

    post_comment = PostComment(
        id=str(ULID()),
        author_id=user.id,
        post_id=post.id,
        content="comment",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    post_comment_repository.save(session, post_comment)
    assert post_comment_repository.find_by_id(session, post_comment.id) is not None

    # when
    response = client.delete(f"/api/posts/{post.id}/comments/{post_comment.id}")

    # then
    assert response.status_code == 204
    assert post_comment_repository.find_by_id(session, post_comment.id) is None


def test_delete_post_comment_with_unauthorized_user(
    session: Session,
    post_repository: IPostRepository,
    post_comment_repository: IPostCommentRepository,
    user: User,
):
    # given
    post = Post(
        id=str(ULID()),
        author_id=str(ULID()),
        title="title",
        content="content",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    post_repository.save(session, post)

    post_comment = PostComment(
        id=str(ULID()),
        author_id=str(ULID()),  # different user
        post_id=post.id,
        content="comment",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    post_comment_repository.save(session, post_comment)

    # when
    response = client.delete(f"/api/posts/{post.id}/comments/{post_comment.id}")

    # then
    assert response.status_code == 403
    assert response.json()["detail"] == "You are not the author of this comment"
