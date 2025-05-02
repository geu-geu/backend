from datetime import UTC, datetime

from app.models import Comment, Post, User


def test_create_comment(client, session, authorized_user):
    # given
    post = Post(
        author_id=authorized_user.id,
        title="test title",
        content="test content",
    )
    session.add(post)
    session.flush()

    # when
    response = client.post(
        f"/api/posts/{post.code}/comments",
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

    comments = [
        Comment(
            post_id=post.id,
            author_id=authorized_user.id,
            content="test comment",
        )
        for _ in range(3)
    ]
    session.add_all(comments)
    session.flush()

    _deleted_comments = [
        Comment(
            post_id=post.id,
            author_id=authorized_user.id,
            content="deleted comment",
            deleted_at=datetime.now(UTC),
        )
        for _ in range(2)
    ]
    session.add_all(_deleted_comments)
    session.flush()

    # when
    response = client.get(f"/api/posts/{post.code}/comments")

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

    comment = Comment(
        post_id=post.id,
        author_id=authorized_user.id,
        content="test comment",
    )
    session.add(comment)
    session.flush()

    # when
    response = client.get(f"/api/posts/{post.code}/comments/{comment.code}")

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

    comment = Comment(
        post_id=post.id,
        author_id=authorized_user.id,
        content="test comment",
    )
    session.add(comment)
    session.flush()

    # when
    response = client.put(
        f"/api/posts/{post.code}/comments/{comment.code}",
        json={"content": "updated comment"},
    )

    # then
    assert response.status_code == 200
    assert response.json()["content"] == "updated comment"


def test_update_comment_403(client, session, authorized_user):
    # given
    post = Post(
        author_id=authorized_user.id,
        title="test title",
        content="test content",
    )
    session.add(post)
    session.flush()

    other_user = User(
        email="other@example.com",
        password="password",
    )
    session.add(other_user)
    session.flush()

    comment = Comment(
        post_id=post.id,
        author_id=other_user.id,  # other user
        content="test comment",
    )
    session.add(comment)
    session.flush()

    # when
    response = client.put(
        f"/api/posts/{post.code}/comments/{comment.code}",
        json={"content": "updated comment"},
    )

    # then
    assert response.status_code == 403


def test_delete_comment(client, session, authorized_user):
    # given
    post = Post(
        author_id=authorized_user.id,
        title="test title",
        content="test content",
    )
    session.add(post)
    session.flush()

    comment = Comment(
        post_id=post.id,
        author_id=authorized_user.id,
        content="test comment",
    )
    session.add(comment)
    session.flush()

    assert comment.deleted_at is None

    # when
    response = client.delete(f"/api/posts/{post.code}/comments/{comment.code}")

    # then
    assert response.status_code == 204
    assert comment.deleted_at is not None


def test_delete_comment_403(client, session, authorized_user):
    # given
    post = Post(
        author_id=authorized_user.id,
        title="test title",
        content="test content",
    )
    session.add(post)
    session.flush()

    other_user = User(
        email="other@example.com",
        password="password",
    )
    session.add(other_user)
    session.flush()

    comment = Comment(
        post_id=post.id,
        author_id=other_user.id,  # other user
        content="test comment",
    )
    session.add(comment)
    session.flush()

    assert comment.deleted_at is None

    # when
    response = client.delete(f"/api/posts/{post.code}/comments/{comment.code}")

    # then
    assert response.status_code == 403
    assert comment.deleted_at is None
