from fastapi import Depends

from src.auth.manager import fastapi_users
from src.models import User


def get_current_user_id(user: User = Depends(fastapi_users.current_user())):
    user_id = user.id
    return user_id
