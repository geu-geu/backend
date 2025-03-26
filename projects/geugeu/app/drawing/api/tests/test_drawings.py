from datetime import UTC, datetime
from unittest.mock import patch

from fastapi import HTTPException, status
from fastapi.testclient import TestClient
from ulid import ULID

from app.drawing.application.drawing_service import DrawingService
from app.drawing.domain.drawing import Drawing, DrawingStatus
from app.drawing.domain.drawing_image import DrawingImage
from app.main import app

client = TestClient(app)


def format_datetime(dt: datetime) -> str:
    return dt.isoformat().replace("+00:00", "Z")


@patch.object(DrawingService, "create_drawing")
def test_create_drawing(create_drawing):
    # given
    post_id = str(ULID())
    content = "Test drawing content"
    image_urls = [
        "https://example.com/image1.png",
        "https://example.com/image2.png",
    ]

    drawing = Drawing(
        id=str(ULID()),
        post_id=post_id,
        author_id=str(ULID()),
        content=content,
        status=DrawingStatus.DRAFT,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    drawing_images = [
        DrawingImage(
            id=str(ULID()),
            drawing_id=drawing.id,
            image_url=image_url,
        )
        for image_url in image_urls
    ]
    create_drawing.return_value = (drawing, drawing_images)

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
    assert response.json() == {
        "id": drawing.id,
        "post_id": drawing.post_id,
        "content": drawing.content,
        "status": drawing.status,
        "images": [image.image_url for image in drawing_images],
        "created_at": format_datetime(drawing.created_at),
        "updated_at": format_datetime(drawing.updated_at),
    }


@patch.object(DrawingService, "get_drawing")
def test_get_drawing(get_drawing):
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
    drawing_images = [
        DrawingImage(
            id=str(ULID()),
            drawing_id=drawing.id,
            image_url="https://example.com/image1.png",
        ),
        DrawingImage(
            id=str(ULID()),
            drawing_id=drawing.id,
            image_url="https://example.com/image2.png",
        ),
    ]
    get_drawing.return_value = (drawing, drawing_images)

    # when
    response = client.get(f"/api/drawings/{drawing.id}")

    # then
    assert response.status_code == 200
    assert response.json() == {
        "id": drawing.id,
        "post_id": drawing.post_id,
        "content": drawing.content,
        "status": drawing.status,
        "images": [image.image_url for image in drawing_images],
        "created_at": format_datetime(drawing.created_at),
        "updated_at": format_datetime(drawing.updated_at),
    }


@patch.object(DrawingService, "get_drawing")
def test_get_drawing_not_found(get_drawing):
    # given
    drawing_id = str(ULID())
    get_drawing.side_effect = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Drawing not found",
    )

    # when
    response = client.get(f"/api/drawings/{drawing_id}")

    # then
    assert response.status_code == 404


@patch.object(DrawingService, "get_drawings_by_post_id")
def test_get_drawings_by_post_id(get_drawings_by_post_id):
    # given
    post_id = str(ULID())
    drawing = Drawing(
        id=str(ULID()),
        post_id=post_id,
        author_id=str(ULID()),
        content="Test drawing content",
        status=DrawingStatus.DRAFT,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    drawing_images = [
        DrawingImage(
            id=str(ULID()),
            drawing_id=drawing.id,
            image_url="https://example.com/image1.png",
        ),
        DrawingImage(
            id=str(ULID()),
            drawing_id=drawing.id,
            image_url="https://example.com/image2.png",
        ),
    ]
    get_drawings_by_post_id.return_value = [(drawing, drawing_images)]

    # when
    response = client.get(f"/api/drawings/by-post/{post_id}")

    # then
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": drawing.id,
            "post_id": drawing.post_id,
            "content": drawing.content,
            "status": drawing.status,
            "images": [image.image_url for image in drawing_images],
            "created_at": format_datetime(drawing.created_at),
            "updated_at": format_datetime(drawing.updated_at),
        }
    ]


@patch.object(DrawingService, "delete_drawing")
def test_delete_drawing(delete_drawing):
    # given
    drawing_id = str(ULID())
    delete_drawing.return_value = None

    # when
    response = client.delete(f"/api/drawings/{drawing_id}")

    # then
    assert response.status_code == 204
    delete_drawing.assert_called_once_with(drawing_id=drawing_id)


@patch.object(DrawingService, "delete_drawing")
def test_delete_drawing_not_found(delete_drawing):
    # given
    drawing_id = str(ULID())
    delete_drawing.side_effect = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Drawing not found",
    )

    # when
    response = client.delete(f"/api/drawings/{drawing_id}")

    # then
    assert response.status_code == 404


@patch.object(DrawingService, "update_drawing")
def test_update_drawing(update_drawing):
    # given
    drawing_id = str(ULID())
    content = "Updated drawing content"
    image_urls = [
        "https://example.com/updated1.png",
        "https://example.com/updated2.png",
    ]

    drawing = Drawing(
        id=drawing_id,
        post_id=str(ULID()),
        author_id=str(ULID()),
        content=content,
        status=DrawingStatus.DRAFT,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    drawing_images = [
        DrawingImage(
            id=str(ULID()),
            drawing_id=drawing.id,
            image_url=image_url,
        )
        for image_url in image_urls
    ]
    update_drawing.return_value = (drawing, drawing_images)

    # when
    response = client.put(
        f"/api/drawings/{drawing_id}",
        json={
            "content": content,
            "image_urls": image_urls,
        },
    )

    # then
    assert response.status_code == 200
    assert response.json() == {
        "id": drawing.id,
        "post_id": drawing.post_id,
        "content": drawing.content,
        "status": drawing.status,
        "images": [image.image_url for image in drawing_images],
        "created_at": format_datetime(drawing.created_at),
        "updated_at": format_datetime(drawing.updated_at),
    }


@patch.object(DrawingService, "update_drawing")
def test_update_drawing_not_found(update_drawing):
    # given
    drawing_id = str(ULID())
    update_drawing.side_effect = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Drawing not found",
    )

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


@patch.object(DrawingService, "complete_drawing")
def test_complete_drawing(complete_drawing):
    # given
    drawing_id = str(ULID())
    content = "Completed drawing content"
    image_urls = [
        "https://example.com/completed1.png",
        "https://example.com/completed2.png",
    ]

    drawing = Drawing(
        id=drawing_id,
        post_id=str(ULID()),
        author_id=str(ULID()),
        content=content,
        status=DrawingStatus.COMPLETED,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
    drawing_images = [
        DrawingImage(
            id=str(ULID()),
            drawing_id=drawing.id,
            image_url=image_url,
        )
        for image_url in image_urls
    ]
    complete_drawing.return_value = (drawing, drawing_images)

    # when
    response = client.post(
        f"/api/drawings/{drawing_id}/complete",
        json={
            "content": content,
            "image_urls": image_urls,
        },
    )

    # then
    assert response.status_code == 200
    assert response.json() == {
        "id": drawing.id,
        "post_id": drawing.post_id,
        "content": drawing.content,
        "status": drawing.status,
        "images": [image.image_url for image in drawing_images],
        "created_at": format_datetime(drawing.created_at),
        "updated_at": format_datetime(drawing.updated_at),
    }


@patch.object(DrawingService, "complete_drawing")
def test_complete_drawing_not_found(complete_drawing):
    # given
    drawing_id = str(ULID())
    complete_drawing.side_effect = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Drawing not found",
    )

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


@patch.object(DrawingService, "complete_drawing")
def test_complete_drawing_already_completed(complete_drawing):
    # given
    drawing_id = str(ULID())
    complete_drawing.side_effect = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Drawing is already completed",
    )

    # when
    response = client.post(
        f"/api/drawings/{drawing_id}/complete",
        json={
            "content": "Completed content",
            "image_urls": ["https://example.com/completed.png"],
        },
    )

    # then
    assert response.status_code == 400
