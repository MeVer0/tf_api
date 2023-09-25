import uvicorn
from fastapi import FastAPI


from src.auth.manager import fastapi_users
from src.auth.schemas import UserRead, UserCreate
from src.auth.manager import auth_backend

from catalog.router import router as catalog_router
from course.router import router as course_router


app = FastAPI()


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)


app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(catalog_router)
app.include_router(course_router)

if __name__ == "__main__":
    uvicorn.run(host="localhost", app=app)