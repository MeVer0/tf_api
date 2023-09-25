from fastapi import APIRouter, Depends

from sqlalchemy import select, func, and_

from src.database import Session, get_session

from src.models import Course, UserCourse

router = APIRouter(
    prefix="/catalog",
    tags=["catalog"]
)


@router.get("")
async def get_catalog(
        session: Session = Depends(get_session),
):
    async with session as conn:
        async with conn.begin():
            catalog = await conn.execute(
                        select(Course.name, Course.logo, Course.price, func.count(UserCourse.user_id).label("active_users_amount")).\
                        select_from(Course).\
                        join(UserCourse, and_(Course.id == UserCourse.course_id, UserCourse.type_id.in_((2, 3))), isouter=True).\
                        group_by(Course.name, Course.logo, Course.price).order_by("active_users_amount")
                )

    return [row._asdict() for row in catalog]