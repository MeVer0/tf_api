from fastapi import APIRouter

from sqlalchemy.orm import aliased
from sqlalchemy import insert, select, delete, update,  case, func
router = APIRouter(
    prefix="/profile",
    tags=["profile"],
)



