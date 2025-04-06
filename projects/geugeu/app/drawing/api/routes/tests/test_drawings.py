from datetime import UTC, datetime
from unittest.mock import Mock

import pytest
from sqlmodel import Session
from ulid import ULID

from app.auth.domain.user import User
from app.drawing.deps import post_repository
from app.drawing.domain.drawing import Drawing, DrawingStatus
from app.drawing.domain.drawing_comment import DrawingComment
from app.drawing.domain.post import Post
from app.drawing.repositories.drawing_comment_repository import (
    IDrawingCommentRepository,
)
from app.drawing.repositories.drawing_repository import IDrawingRepository
from app.drawing.repositories.post_repository import IPostRepository
from app.main import app


@pytest.fixture()
def override_post_repository():
    def _post_repository():
        mock = Mock(spec=IPostRepository)
        mock.find_by_id.side_effect = lambda session, id: Post(id=id)
        return mock

    app.dependency_overrides[post_repository] = _post_repository
    yield
    app.dependency_overrides.clear()


def test_create_drawing(client, override_post_repository):
    # given
    post_id = str(ULID())
    content = "Test drawing content"
    image_urls = [
        "https://example.com/image1.png",
        "https://example.com/image2.png",
    ]

    # when
    response = client.post(
        "/api/drawings/",
        json={
            "post_id": post_id,
            "content": content,
            "image_urls": image_urls,
        },
    )

    # then
    assert response.status_code == 201
    assert response.json()["post_id"] == post_id
    assert response.json()["content"] == content
    assert response.json()["status"] == DrawingStatus.DRAFT
    assert response.json()["images"] == image_urls


def test_get_drawing(client, drawing_repository: IDrawingRepository, session: Session):
    # given
    drawing = Drawing(
        id=str(ULID()),
        post_id=str(ULID()),
        author_id=str(ULID()),
        content="Test drawing content",
        status=DrawingStatus.DRAFT,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    drawing_repository.save(session, drawing)

    # when
    response = client.get(f"/api/drawings/{drawing.id}")

    # then
    assert response.status_code == 200
    assert response.json()["id"] == drawing.id
    assert response.json()["post_id"] == drawing.post_id
    assert response.json()["content"] == drawing.content
    assert response.json()["status"] == drawing.status
    assert response.json()["images"] == []


def test_get_drawing_not_found(client):
    # given
    drawing_id = str(ULID())

    # when
    response = client.get(f"/api/drawings/{drawing_id}")

    # then
    assert response.status_code == 404


def test_get_drawings_by_post_id(
    client, session: Session, drawing_repository: IDrawingRepository
):
    # given
    post_id = str(ULID())
    drawing1 = Drawing(
        id=str(ULID()),
        post_id=post_id,
        author_id=str(ULID()),
        content="Test drawing content",
        status=DrawingStatus.DRAFT,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    drawing2 = Drawing(
        id=str(ULID()),
        post_id=post_id,
        author_id=str(ULID()),
        content="Test drawing content 2",
        status=DrawingStatus.DRAFT,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    drawing3 = Drawing(
        id=str(ULID()),
        post_id=str(ULID()),  # 다른 포스트의 드로잉
        author_id=str(ULID()),
        content="Test drawing content 3",
        status=DrawingStatus.DRAFT,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    drawing_repository.save(session, drawing1)
    drawing_repository.save(session, drawing2)
    drawing_repository.save(session, drawing3)
    # when
    response = client.get(f"/api/drawings/by-post/{post_id}")

    # then
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_delete_drawing(
    client, session: Session, drawing_repository: IDrawingRepository
):
    # given
    drawing = Drawing(
        id=str(ULID()),
        post_id=str(ULID()),
        author_id=str(ULID()),
        content="Test drawing content",
        status=DrawingStatus.DRAFT,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    drawing_repository.save(session, drawing)
    assert drawing_repository.find_by_id(session, drawing.id) is not None

    # when
    response = client.delete(f"/api/drawings/{drawing.id}")

    # then
    assert response.status_code == 204
    assert drawing_repository.find_by_id(session, drawing.id) is None


def test_delete_drawing_not_found(client):
    # given
    drawing_id = str(ULID())

    # when
    response = client.delete(f"/api/drawings/{drawing_id}")

    # then
    assert response.status_code == 404


def test_update_drawing(
    client, session: Session, drawing_repository: IDrawingRepository
):
    # given
    drawing = Drawing(
        id=str(ULID()),
        post_id=str(ULID()),
        author_id=str(ULID()),
        content="Test drawing content",
        status=DrawingStatus.DRAFT,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    drawing_repository.save(session, drawing)

    new_content = "Updated drawing content"
    new_image_urls = [
        "https://example.com/updated1.png",
        "https://example.com/updated2.png",
    ]

    # when
    response = client.put(
        f"/api/drawings/{drawing.id}",
        json={
            "content": new_content,
            "image_urls": new_image_urls,
        },
    )

    # then
    assert response.status_code == 200
    assert response.json()["id"] == drawing.id
    assert response.json()["post_id"] == drawing.post_id
    assert response.json()["content"] == new_content
    assert response.json()["status"] == DrawingStatus.DRAFT
    assert response.json()["images"] == new_image_urls


def test_update_drawing_not_found(client):
    # given
    drawing_id = str(ULID())

    # when
    response = client.put(
        f"/api/drawings/{drawing_id}",
        json={
            "content": "Updated content",
            "image_urls": ["https://example.com/updated.png"],
        },
    )

    # then
    assert response.status_code == 404


def test_complete_drawing(
    client, session: Session, drawing_repository: IDrawingRepository
):
    # given
    drawing = Drawing(
        id=str(ULID()),
        post_id=str(ULID()),
        author_id=str(ULID()),
        content="Test drawing content",
        status=DrawingStatus.DRAFT,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    drawing_repository.save(session, drawing)

    # when
    response = client.post(
        f"/api/drawings/{drawing.id}/complete",
        json={
            "content": "Completed content",
            "image_urls": ["https://example.com/completed.png"],
        },
    )

    # then
    assert response.status_code == 200
    assert response.json()["id"] == drawing.id
    assert response.json()["post_id"] == drawing.post_id
    assert response.json()["content"] == "Completed content"
    assert response.json()["status"] == DrawingStatus.COMPLETED
    assert response.json()["images"] == ["https://example.com/completed.png"]


def test_complete_drawing_not_found(client):
    # given
    drawing_id = str(ULID())

    # when
    response = client.post(
        f"/api/drawings/{drawing_id}/complete",
        json={
            "content": "Completed content",
            "image_urls": ["https://example.com/completed.png"],
        },
    )

    # then
    assert response.status_code == 404


def test_complete_drawing_already_completed(
    client, session: Session, drawing_repository: IDrawingRepository
):
    # given
    drawing = Drawing(
        id=str(ULID()),
        post_id=str(ULID()),
        author_id=str(ULID()),
        content="Test drawing content",
        status=DrawingStatus.COMPLETED,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    drawing_repository.save(session, drawing)

    # when
    response = client.post(
        f"/api/drawings/{drawing.id}/complete",
        json={
            "content": "Completed content",
            "image_urls": ["https://example.com/completed.png"],
        },
    )

    # then
    assert response.status_code == 400
    assert response.json()["detail"] == "Drawing is already completed"


def test_create_drawing_comment(
    client,
    session: Session,
    drawing_repository: IDrawingRepository,
    user: User,
):
    # given
    drawing = Drawing(
        id=str(ULID()),
        author_id=str(ULID()),
        post_id=str(ULID()),
        content="content",
        status=DrawingStatus.DRAFT,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    drawing_repository.save(session, drawing)

    # when
    response = client.post(
        f"/api/drawings/{drawing.id}/comments",
        json={"content": "comment"},
    )

    # then
    assert response.status_code == 201
    assert response.json()["id"] is not None
    assert response.json()["author_id"] == user.id
    assert response.json()["drawing_id"] == drawing.id
    assert response.json()["content"] == "comment"


def test_get_drawing_comments(
    client,
    session: Session,
    drawing_repository: IDrawingRepository,
    drawing_comment_repository: IDrawingCommentRepository,
    user: User,
):
    # given
    drawing = Drawing(
        id=str(ULID()),
        author_id=str(ULID()),
        post_id=str(ULID()),
        content="content",
        status=DrawingStatus.DRAFT,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    drawing_repository.save(session, drawing)

    drawing_comment = DrawingComment(
        id=str(ULID()),
        author_id=str(ULID()),
        drawing_id=drawing.id,
        content="comment",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    drawing_comment_repository.save(session, drawing_comment)

    # when
    response = client.get(f"/api/drawings/{drawing.id}/comments")

    # then
    assert response.status_code == 200
    assert response.json()[0]["id"] == drawing_comment.id
    assert response.json()[0]["author_id"] == drawing_comment.author_id
    assert response.json()[0]["drawing_id"] == drawing_comment.drawing_id
    assert response.json()[0]["content"] == drawing_comment.content


def test_update_drawing_comment(
    client,
    session: Session,
    drawing_repository: IDrawingRepository,
    drawing_comment_repository: IDrawingCommentRepository,
    user: User,
):
    # given
    drawing = Drawing(
        id=str(ULID()),
        author_id=str(ULID()),
        post_id=str(ULID()),
        content="content",
        status=DrawingStatus.DRAFT,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    drawing_repository.save(session, drawing)

    drawing_comment = DrawingComment(
        id=str(ULID()),
        author_id=user.id,
        drawing_id=drawing.id,
        content="original comment",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    drawing_comment_repository.save(session, drawing_comment)

    # when
    response = client.put(
        f"/api/drawings/{drawing.id}/comments/{drawing_comment.id}",
        json={"content": "updated comment"},
    )

    # then
    assert response.status_code == 200
    assert response.json()["id"] == drawing_comment.id
    assert response.json()["author_id"] == drawing_comment.author_id
    assert response.json()["drawing_id"] == drawing_comment.drawing_id
    assert response.json()["content"] == "updated comment"


def test_update_drawing_comment_with_unauthorized_user(
    client,
    session: Session,
    drawing_repository: IDrawingRepository,
    drawing_comment_repository: IDrawingCommentRepository,
    user: User,
):
    # given
    drawing = Drawing(
        id=str(ULID()),
        author_id=str(ULID()),
        post_id=str(ULID()),
        content="content",
        status=DrawingStatus.DRAFT,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    drawing_repository.save(session, drawing)

    drawing_comment = DrawingComment(
        id=str(ULID()),
        author_id=str(ULID()),  # different user
        drawing_id=drawing.id,
        content="comment",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    drawing_comment_repository.save(session, drawing_comment)

    # when
    response = client.put(
        f"/api/drawings/{drawing.id}/comments/{drawing_comment.id}",
        json={"content": "updated comment"},
    )

    # then
    assert response.status_code == 403
    assert response.json()["detail"] == "You are not the author of this comment"


def test_delete_drawing_comment(
    client,
    session: Session,
    drawing_repository: IDrawingRepository,
    drawing_comment_repository: IDrawingCommentRepository,
    user: User,
):
    # given
    drawing = Drawing(
        id=str(ULID()),
        author_id=str(ULID()),
        post_id=str(ULID()),
        content="content",
        status=DrawingStatus.DRAFT,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    drawing_repository.save(session, drawing)

    drawing_comment = DrawingComment(
        id=str(ULID()),
        author_id=user.id,
        drawing_id=drawing.id,
        content="comment",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    drawing_comment_repository.save(session, drawing_comment)
    assert (
        drawing_comment_repository.find_by_id(session, drawing_comment.id) is not None
    )

    # when
    response = client.delete(
        f"/api/drawings/{drawing.id}/comments/{drawing_comment.id}"
    )

    # then
    assert response.status_code == 204
    assert drawing_comment_repository.find_by_id(session, drawing_comment.id) is None


def test_delete_drawing_comment_with_unauthorized_user(
    client,
    session: Session,
    drawing_repository: IDrawingRepository,
    drawing_comment_repository: IDrawingCommentRepository,
    user: User,
):
    # given
    drawing = Drawing(
        id=str(ULID()),
        author_id=str(ULID()),
        post_id=str(ULID()),
        content="content",
        status=DrawingStatus.DRAFT,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    drawing_repository.save(session, drawing)

    drawing_comment = DrawingComment(
        id=str(ULID()),
        author_id=str(ULID()),  # different user
        drawing_id=drawing.id,
        content="comment",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    drawing_comment_repository.save(session, drawing_comment)

    # when
    response = client.delete(
        f"/api/drawings/{drawing.id}/comments/{drawing_comment.id}"
    )

    # then
    assert response.status_code == 403
    assert response.json()["detail"] == "You are not the author of this comment"
