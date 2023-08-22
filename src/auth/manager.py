from src.auth.database import get_user_db
from src.models import User
from src.auth.config import secret

from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy
from fastapi_users import BaseUserManager, IntegerIDMixin, FastAPIUsers
from fastapi import Depends, Request

from typing import Optional

from src.auth.utils import MS

cookie_transport = CookieTransport(cookie_max_age=3600)
SECRET = secret


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(IntegerIDMixin, BaseUserManager[User, IntegerIDMixin]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        MS.send_mail(
            destination=user.email,
            subject="Перейдите по ссылке, чтобы завершить регистрацию!",
            content=f""""Ваш токен: http://127.0.0.1:8000/auth/verify?token={token}
                         """

        )
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)