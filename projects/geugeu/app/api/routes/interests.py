from fastapi import APIRouter, Query

from app.api.dependencies import CurrentUserDep, CurrentUserOptionalDep
from app.core.dependencies import InterestServiceDep
from app.schemas.interests import InterestListSchema, InterestResponseSchema

router = APIRouter()


@router.post("/posts/{post_code}/interests", response_model=InterestResponseSchema)
async def toggle_interest(
    post_code: str,
    current_user: CurrentUserDep,
    service: InterestServiceDep,
):
    return service.toggle_interest(current_user, post_code)


@router.get(
    "/posts/{post_code}/interests",
    response_model=InterestListSchema,
    response_model_exclude_none=True,
)
async def get_post_interests(
    post_code: str,
    current_user: CurrentUserOptionalDep,
    service: InterestServiceDep,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=0, le=100),
):
    return service.get_post_interests(post_code, current_user, page, page_size)


@router.get(
    "/users/{user_code}/interests",
    response_model=InterestListSchema,
    response_model_exclude_none=True,
)
async def get_user_interests(
    user_code: str,
    service: InterestServiceDep,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    return service.get_user_interests(user_code, page, page_size)
