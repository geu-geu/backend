from fastapi import APIRouter

router = APIRouter()


@router.post("/{post_code}/comments")
async def create_comment(post_code: str):
    raise NotImplementedError


@router.get("/{post_code}/comments")
async def get_comments(post_code: str):
    raise NotImplementedError


@router.get("/{post_code}/comments/{comment_code}")
async def get_comment(post_code: str, comment_code: str):
    raise NotImplementedError


@router.put("/{post_code}/comments/{comment_code}")
async def update_comment(post_code: str, comment_code: str):
    raise NotImplementedError


@router.delete("/{post_code}/comments/{comment_code}")
async def delete_comment(post_code: str, comment_code: str):
    raise NotImplementedError
