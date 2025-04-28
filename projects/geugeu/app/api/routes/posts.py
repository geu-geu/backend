from fastapi import APIRouter

router = APIRouter()


@router.post("")
async def create_post():
    raise NotImplementedError


@router.get("")
async def get_posts():
    raise NotImplementedError


@router.get("/{post_code}")
async def get_post(post_code: str):
    raise NotImplementedError


@router.put("/{post_code}")
async def update_post(post_code: str):
    raise NotImplementedError


@router.delete("/{post_code}")
async def delete_post(post_code: str):
    raise NotImplementedError
