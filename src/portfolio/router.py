from fastapi import APIRouter, Depends
from sqlalchemy import insert, select, delete, update

from src.database import Session, get_session
from src.auth.dependencies import get_current_user_id
from src.portfolio.models import Portfolio, PortfolioProgramLang, PortfolioDatabase, PortfolioKnowledgeField
from src.models import DicProgramLang, DicDatabase, DicKnowledgeField
from src.portfolio.schemas import CreatePortfolio, EditPortfolio

from src.auth.manager import fastapi_users


router = APIRouter(
     prefix="/portfolio",
     tags=["portfolio"],
     dependencies=[Depends(fastapi_users.current_user(active=True, verified=True))]
)


@router.post("/create")
async def create_portfolio(request: CreatePortfolio,
                           user_id: int = Depends(get_current_user_id),
                           session: Session = Depends(get_session),
                           ):

    request = request.dict()

    async with session as conn:
        async with conn.begin():
            await conn.execute(
                insert(Portfolio).values(request))

    async with session as conn:
        async with conn.begin():
            portfolio_id = await conn.execute(
                select(Portfolio.id).where(Portfolio.user_id == user_id).order_by(Portfolio.date_create.desc()).limit(1)
            )

            portfolio_id = portfolio_id.scalar()

            await conn.execute(
            insert(PortfolioProgramLang).
                from_select(["portfolio_id", "program_lang_id"],
                            select(portfolio_id, DicProgramLang.id).where(DicProgramLang.name.in_(request.program_lang))
                            )
            )

            await conn.execute(
            insert(PortfolioDatabase).
                from_select(["portfolio_id", "database_id"],
                            select(portfolio_id, DicDatabase.id).where(DicDatabase.name.in_(request.database))
                            )
            )

            await conn.execute(
                insert(PortfolioKnowledgeField).
                    from_select(["portfolio_id", "knowledge_field_id"],
                                select(portfolio_id, DicKnowledgeField.id).where(DicKnowledgeField.name.in_(request.knowledge_field))
                                )
            )

    return


@router.post("/delete")
async def delete_portfolio(portfolio_id: int,
                           session: Session = Depends(get_session),
                           ):

    async with session as conn:
        async with conn.begin():
            await conn.execute(
                delete(Portfolio).where(Portfolio.id == portfolio_id)
            )


@router.post("/edit")
async def edit_profile(request: EditPortfolio,
                       session: Session = Depends(get_session),
                       ):

    request = request.dict()

    async with session as conn:
        async with conn.begin():
            await conn.execute(
                update(Portfolio).where(Portfolio.id == request.get("portfolio_id")).values(
                                hh_link=request['portfolio']["hh_link"],
                                linkedin_link=request['portfolio']["linkedin_link"],
                                github_link=request['portfolio']["github_link"]
                )
            )
    return
