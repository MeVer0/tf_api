from fastapi import APIRouter, Depends

from sqlalchemy import insert, select

from src.auth.dependencies import get_current_user_id
from src.database import engine
from src.portfolio.models import Portfolio, PortfolioProgramLang, PortfolioDatabase, PortfolioKnowledgeField
from src.portfolio.schemas import Portfolio as ps

from src.auth.manager import fastapi_users


router = APIRouter(
     prefix="/portfolio",
     tags=["portfolio"],
     dependencies=[Depends(fastapi_users.current_user(active=True, verified=True))]
)


@router.post("/create")
async def create_portfolio(request: ps, user_id: int = Depends(get_current_user_id)):

    request = dict(request)
    request["user_id"] = user_id

    async with engine.begin() as conn:
        await conn.execute(
            insert(Portfolio).values(request))

    async with engine.begin() as conn:
        portfolio_id = await conn.execute(
            select(Portfolio).where(Portfolio.user_id == user_id).order_by(Portfolio.id.desc()).limit(1)
        )

        await conn.execute(
            insert(PortfolioProgramLang).values(request.values()["program_lang"])
        )

        await conn.execute(
            insert(PortfolioKnowledgeField).values(request.values()["knowledge_field"])
        )

        await conn.execute(
            insert(PortfolioDatabase).values(request.values().get("database"))
        )
    return
