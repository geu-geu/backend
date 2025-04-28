from fastapi import APIRouter

router = APIRouter()


@router.post("")
async def create_drawing():
    raise NotImplementedError


@router.get("")
async def get_drawings():
    raise NotImplementedError


@router.get("/{drawing_code}")
async def get_drawing(drawing_code: str):
    raise NotImplementedError


@router.put("/{drawing_code}")
async def update_drawing(drawing_code: str):
    raise NotImplementedError


@router.delete("/{drawing_code}")
async def delete_drawing(drawing_code: str):
    raise NotImplementedError
