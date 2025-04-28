from fastapi import APIRouter

router = APIRouter()


@router.post("")
async def sign_up():
    raise NotImplementedError


@router.get("/me")
async def get_me():
    raise NotImplementedError


@router.put("/me")
async def update_me():
    raise NotImplementedError


@router.delete("/me")
async def delete_me():
    raise NotImplementedError
