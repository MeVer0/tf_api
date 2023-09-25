from fastapi import APIRouter, Depends

from sqlalchemy import select, func, and_

from sqlalchemy.dialects.mysql import insert

from src.database import Session, get_session
from src.auth.dependencies import get_current_user_id

from src.models import Course, UserCourse


router = APIRouter(
    prefix="/course",
    tags=["course"]
)


@router.get("")
async def get_course(
        id: int,
        session: Session = Depends(get_session)
):

    async with session as conn:
        async with conn.begin():
            course = await conn.execute(
                        select(Course.name, Course.logo, Course.price, Course.description, func.count(UserCourse.user_id).label("active_users_amount")).\
                        select_from(Course).\
                        join(UserCourse, and_(Course.id == UserCourse.course_id, UserCourse.type_id.in_((2, 3)), Course.id == id), isouter=True).\
                        group_by(Course.name, Course.logo, Course.price, Course.description).order_by("active_users_amount")
                )

        return [row._asdict() for row in course]


@router.post("/try_for_free")
async def try_for_free(
    course_id: int,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id)
):
    async with session as conn:
        async with conn.begin():
            if user_id:
                await conn.execute(
                    insert(UserCourse).values(user_id=user_id, course_id=course_id, type_id=4).prefix_with('IGNORE')
                )
            else:
                return "Сперва нужно зарегестрироваться. Если аккаунт уже есть, то залогиньтесь"


@router.post("/add_to_wish_list")
async def add_to_wish_list(
        course_id: int,
        session: Session = Depends(get_session),
        user_id: int = Depends(get_current_user_id)
):
    async with session as conn:
        async with conn.begin():
            if user_id:
                await conn.execute(
                    insert(UserCourse).values(user_id=user_id, course_id=course_id, type_id=1).prefix_with('IGNORE').on_duplicate_key_update(type_id=1)
                )
            else:
                return "Сперва нужно зарегестрироваться. Если аккаунт уже есть, то залогиньтесь"


