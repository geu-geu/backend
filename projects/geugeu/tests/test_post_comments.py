from datetime import UTC, datetime

from app.models import Comment, Post, User


def test_create_comment(client, db, authorized_user):
    # given
    post = Post(
        author_id=authorized_user.id,
        title="test title",
        content="test content",
    )
    db.add(post)
    db.flush()

    # when
    response = client.post(
        f"/api/posts/{post.code}/comments",
        json={"content": "test comment"},
    )

    # then
    assert response.status_code == 201
    assert response.json()["content"] == "test comment"


def test_create_comment_401(client, user):
    # when
    response = client.post(
        "/api/posts/abcd123/comments",
        json={"content": "test comment"},
    )

    # then
    assert response.status_code == 401


def test_create_comment_404(client, authorized_user):
    # when
    response = client.post(
        "/api/posts/abcd123/comments",
        json={"content": "test comment"},
    )

    # then
    assert response.status_code == 404


def test_get_comments(client, db, authorized_user):
    # given
    post = Post(
        author_id=authorized_user.id,
        title="test title",
        content="test content",
    )
    db.add(post)
    db.flush()

    comments = [
        Comment(
            post_id=post.id,
            author_id=authorized_user.id,
            content="test comment",
        )
        for _ in range(3)
    ]
    db.add_all(comments)
    db.flush()

    _deleted_comments = [
        Comment(
            post_id=post.id,
            author_id=authorized_user.id,
            content="deleted comment",
            deleted_at=datetime.now(UTC),
        )
        for _ in range(2)
    ]
    db.add_all(_deleted_comments)
    db.flush()

    # when
    response = client.get(f"/api/posts/{post.code}/comments")

    # then
    assert response.status_code == 200
    assert response.json()["count"] == 3
    assert len(response.json()["items"]) == 3


def test_get_comments_401(client, user):
    # when
    response = client.get("/api/posts/abcd123/comments")

    # then
    assert response.status_code == 401


def test_get_comments_404(client, authorized_user):
    # when
    response = client.get("/api/posts/abcd123/comments")

    # then
    assert response.status_code == 404


def test_get_comment(client, db, authorized_user):
    # given
    post = Post(
        author_id=authorized_user.id,
        title="test title",
        content="test content",
    )
    db.add(post)
    db.flush()

    comment = Comment(
        post_id=post.id,
        author_id=authorized_user.id,
        content="test comment",
    )
    db.add(comment)
    db.flush()

    # when
    response = client.get(f"/api/posts/{post.code}/comments/{comment.code}")

    # then
    assert response.status_code == 200
    assert response.json()["content"] == "test comment"
    assert response.json()["author"]["code"] == authorized_user.code


def test_get_comment_401(client, user):
    # when
    response = client.get("/api/posts/abcd123/comments/abcd123")

    # then
    assert response.status_code == 401


def test_get_comment_404(client, authorized_user):
    # when
    response = client.get("/api/posts/abcd123/comments/abcd123")

    # then
    assert response.status_code == 404


def test_update_comment(client, db, authorized_user):
    # given
    post = Post(
        author_id=authorized_user.id,
        title="test title",
        content="test content",
    )
    db.add(post)
    db.flush()

    comment = Comment(
        post_id=post.id,
        author_id=authorized_user.id,
        content="test comment",
    )
    db.add(comment)
    db.flush()

    # when
    response = client.put(
        f"/api/posts/{post.code}/comments/{comment.code}",
        json={"content": "updated comment"},
    )

    # then
    assert response.status_code == 200
    assert response.json()["content"] == "updated comment"


def test_update_comment_401(client, user):
    # when
    response = client.put(
        "/api/posts/abcd123/comments/abcd123",
        json={"content": "updated comment"},
    )

    # then
    assert response.status_code == 401


def test_update_comment_403(client, db, authorized_user):
    # given
    post = Post(
        author_id=authorized_user.id,
        title="test title",
        content="test content",
    )
    db.add(post)
    db.flush()

    other_user = User(
        email="other@example.com",
        password="password",
    )
    db.add(other_user)
    db.flush()

    comment = Comment(
        post_id=post.id,
        author_id=other_user.id,  # other user
        content="test comment",
    )
    db.add(comment)
    db.flush()

    # when
    response = client.put(
        f"/api/posts/{post.code}/comments/{comment.code}",
        json={"content": "updated comment"},
    )

    # then
    assert response.status_code == 403


def test_update_comment_404(client, authorized_user):
    # when
    response = client.put(
        "/api/posts/abcd123/comments/abcd123",
        json={"content": "updated comment"},
    )

    # then
    assert response.status_code == 404


def test_delete_comment(client, db, authorized_user):
    # given
    post = Post(
        author_id=authorized_user.id,
        title="test title",
        content="test content",
    )
    db.add(post)
    db.flush()

    comment = Comment(
        post_id=post.id,
        author_id=authorized_user.id,
        content="test comment",
    )
    db.add(comment)
    db.flush()

    assert comment.deleted_at is None

    # when
    response = client.delete(f"/api/posts/{post.code}/comments/{comment.code}")

    # then
    assert response.status_code == 204
    assert comment.deleted_at is not None


def test_delete_comment_401(client, user):
    # when
    response = client.delete("/api/posts/abcd123/comments/abcd123")

    # then
    assert response.status_code == 401


def test_delete_comment_403(client, db, authorized_user):
    # given
    post = Post(
        author_id=authorized_user.id,
        title="test title",
        content="test content",
    )
    db.add(post)
    db.flush()

    other_user = User(
        email="other@example.com",
        password="password",
    )
    db.add(other_user)
    db.flush()

    comment = Comment(
        post_id=post.id,
        author_id=other_user.id,  # other user
        content="test comment",
    )
    db.add(comment)
    db.flush()

    assert comment.deleted_at is None

    # when
    response = client.delete(f"/api/posts/{post.code}/comments/{comment.code}")

    # then
    assert response.status_code == 403
    assert comment.deleted_at is None


def test_delete_comment_404(client, authorized_user):
    # when
    response = client.delete("/api/posts/abcd123/comments/abcd123")

    # then
    assert response.status_code == 404


def test_create_reply_comment(client, db, authorized_user):
    # given
    post = Post(
        author_id=authorized_user.id,
        title="test title",
        content="test content",
    )
    db.add(post)
    db.flush()

    comment = Comment(
        post_id=post.id,
        author_id=authorized_user.id,
        content="test comment",
    )
    db.add(comment)
    db.flush()

    # when
    response = client.post(
        f"/api/posts/{post.code}/comments",
        json={"content": "test reply", "parent_code": comment.code},
    )

    # then
    assert response.status_code == 201
    assert response.json()["content"] == "test reply"
