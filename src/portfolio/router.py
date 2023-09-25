from typing import List

from fastapi import APIRouter, Depends, Query
from pydantic import parse_obj_as

from sqlalchemy import insert, select, delete, update,  case, func
from sqlalchemy.orm import aliased

from src.database import Session, get_session
from src.auth.dependencies import get_current_user_id
from src.portfolio.models import Portfolio, PortfolioProgramLang, PortfolioDatabase, PortfolioKnowledgeField
from src.models import DicProgramLang, DicDatabase, DicKnowledgeField, User
from src.portfolio.schemas import CreatePortfolio, EditPortfolio, GetPortfolio

from src.auth.manager import fastapi_users


router = APIRouter(
     prefix="/portfolio",
     tags=["portfolio"],
     #dependencies=[Depends(fastapi_users.current_user(active=True, verified=True))]
)


@router.post("/create")
async def create_portfolio(request: CreatePortfolio,
                           user_id: int = Depends(get_current_user_id),
                           session: Session = Depends(get_session),
                           ):

    request = request.dict()
    portfolio_user = request["portfolio"]
    portfolio_user["user_id"] = user_id

    async with session as conn:
        async with conn.begin():
            await conn.execute(
                insert(Portfolio).values(portfolio_user, ))

    async with session as conn:
        async with conn.begin():
            portfolio_id = await conn.execute(
                select(Portfolio.id).where(Portfolio.user_id == user_id).order_by(Portfolio.date_create.desc()).limit(1)
            )

            portfolio_id = portfolio_id.scalar()

            await conn.execute(
            insert(PortfolioProgramLang).
                from_select(["portfolio_id", "program_lang_id"],
                            select(portfolio_id, DicProgramLang.id).where(DicProgramLang.name.in_(request["program_lang"]))
                            )
            )

            await conn.execute(
            insert(PortfolioDatabase).
                from_select(["portfolio_id", "database_id"],
                            select(portfolio_id, DicDatabase.id).where(DicDatabase.name.in_(request["database"]))
                            )
            )

            await conn.execute(
                insert(PortfolioKnowledgeField).
                    from_select(["portfolio_id", "knowledge_field_id"],
                                select(portfolio_id, DicKnowledgeField.id).where(DicKnowledgeField.name.in_(request["knowledge_field"]))
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


@router.get("/search", response_model=List[GetPortfolio])
async def get_search_portfolio(
        portfolio_knowledge_field_list: List[int] = Query(None),
        portfolio_program_lang_list: List[int] = Query(None),
        portfolio_database_list: List[int] = Query(None),
        session: Session = Depends(get_session),
):
    async with session as conn:
        async with conn.begin():

            if portfolio_knowledge_field_list is None:
                portfolio_knowledge_field_list = select(DicKnowledgeField.id).subquery()
            if portfolio_program_lang_list is None:
                portfolio_program_lang_list = select(DicProgramLang.id).subquery()
            if portfolio_database_list is None:
                portfolio_database_list = select(DicDatabase.id).subquery()

            p = aliased(Portfolio)
            pd = aliased(PortfolioDatabase)
            pkf = aliased(PortfolioKnowledgeField)
            ppl = aliased(PortfolioProgramLang)

            result = await session.execute(
                select(
                func.sum(
                    case(
                        (pd.database_id.in_(portfolio_database_list), 1),
                        (pkf.knowledge_field_id.in_(portfolio_knowledge_field_list), 1),
                        (ppl.program_lang_id.in_(portfolio_program_lang_list), 1),
                        else_=0
                    )
                ).label('kr'),
                p.user_id,
                p.id,
                func.group_concat(pd.database_id.distinct()).label('database_id'),
                func.group_concat(pkf.knowledge_field_id.distinct()).label('knowledge_field_id'),
                func.group_concat(ppl.program_lang_id.distinct()).label('program_lang_id')
            ).select_from(p)\
                .join(pd, p.id == pd.portfolio_id)\
                .join(pkf, p.id == pkf.portfolio_id)\
                .join(ppl, p.id == ppl.portfolio_id)\
                .filter(pd.database_id.in_(portfolio_database_list))\
                .filter(pkf.knowledge_field_id.in_(portfolio_knowledge_field_list))\
                .filter(ppl.program_lang_id.in_(portfolio_program_lang_list))\
                .group_by(p.user_id, p.id)\
                .order_by(
                    func.sum(
                            case(
                                (pd.database_id.in_(portfolio_database_list), 1),
                                (pkf.knowledge_field_id.in_(portfolio_knowledge_field_list), 1),
                                (ppl.program_lang_id.in_(portfolio_program_lang_list), 1),
                                else_=0
                                )
                            ).desc()
                        )
            )

            result_dicts = [row._asdict() for row in result]

            return parse_obj_as(List[GetPortfolio], result_dicts)



