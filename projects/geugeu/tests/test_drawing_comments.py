from app.models import Comment, Drawing, Post


def test_create_comment(client, session, authorized_user):
    # given
    post = Post(
        author_id=authorized_user.id,
        title="test title",
        content="test content",
    )
    session.add(post)
    session.flush()

    drawing = Drawing(
        post_id=post.id,
        author_id=authorized_user.id,
        content="test content",
    )
    session.add(drawing)
    session.flush()

    # when
    response = client.post(
        f"/api/drawings/{drawing.code}/comments",
        json={"content": "test comment"},
    )

    # then
    assert response.status_code == 201
    assert response.json()["content"] == "test comment"


def test_get_comments(client, session, authorized_user):
    # given
    post = Post(
        author_id=authorized_user.id,
        title="test title",
        content="test content",
    )
    session.add(post)
    session.flush()

    drawing = Drawing(
        post_id=post.id,
        author_id=authorized_user.id,
        content="test content",
    )
    session.add(drawing)
    session.flush()

    comments = [
        Comment(
            drawing_id=drawing.id,
            author_id=authorized_user.id,
            content="test comment",
        )
        for _ in range(3)
    ]
    session.add_all(comments)
    session.flush()

    # when
    response = client.get(f"/api/drawings/{drawing.code}/comments")

    # then
    assert response.status_code == 200
    assert response.json()["count"] == 3
    assert len(response.json()["items"]) == 3


def test_get_comment(client, session, authorized_user):
    # given
    post = Post(
        author_id=authorized_user.id,
        title="test title",
        content="test content",
    )
    session.add(post)
    session.flush()

    drawing = Drawing(
        post_id=post.id,
        author_id=authorized_user.id,
        content="test content",
    )
    session.add(drawing)
    session.flush()

    comment = Comment(
        drawing_id=drawing.id,
        author_id=authorized_user.id,
        content="test comment",
    )
    session.add(comment)
    session.flush()

    # when
    response = client.get(f"/api/drawings/{drawing.code}/comments/{comment.code}")

    # then
    assert response.status_code == 200
    assert response.json()["content"] == "test comment"
    assert response.json()["author"]["code"] == authorized_user.code


def test_update_comment(client, session, authorized_user):
    # given
    post = Post(
        author_id=authorized_user.id,
        title="test title",
        content="test content",
    )
    session.add(post)
    session.flush()

    drawing = Drawing(
        post_id=post.id,
        author_id=authorized_user.id,
        content="test content",
    )
    session.add(drawing)
    session.flush()

    comment = Comment(
        drawing_id=drawing.id,
        author_id=authorized_user.id,
        content="test comment",
    )
    session.add(comment)
    session.flush()

    # when
    response = client.put(
        f"/api/drawings/{drawing.code}/comments/{comment.code}",
        json={"content": "updated comment"},
    )

    # then
    assert response.status_code == 200
    assert response.json()["content"] == "updated comment"


def test_delete_comment(client, session, authorized_user):
    # given
    post = Post(
        author_id=authorized_user.id,
        title="test title",
        content="test content",
    )
    session.add(post)
    session.flush()

    drawing = Drawing(
        post_id=post.id,
        author_id=authorized_user.id,
        content="test content",
    )
    session.add(drawing)
    session.flush()

    comment = Comment(
        drawing_id=drawing.id,
        author_id=authorized_user.id,
        content="test comment",
    )
    session.add(comment)
    session.flush()

    assert comment.deleted_at is None

    # when
    response = client.delete(f"/api/drawings/{drawing.code}/comments/{comment.code}")

    # then
    assert response.status_code == 204
    assert comment.deleted_at is not None
