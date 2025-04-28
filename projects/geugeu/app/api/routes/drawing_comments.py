from fastapi import APIRouter

router = APIRouter()


@router.post("/{drawing_code}/comments")
async def create_comment(drawing_code: str):
    raise NotImplementedError


@router.get("/{drawing_code}/comments")
async def get_comments(drawing_code: str):
    raise NotImplementedError


@router.get("/{drawing_code}/comments/{comment_code}")
async def get_comment(drawing_code: str, comment_code: str):
    raise NotImplementedError


@router.put("/{drawing_code}/comments/{comment_code}")
async def update_comment(drawing_code: str, comment_code: str):
    raise NotImplementedError


@router.delete("/{drawing_code}/comments/{comment_code}")
async def delete_comment(drawing_code: str, comment_code: str):
    raise NotImplementedError
