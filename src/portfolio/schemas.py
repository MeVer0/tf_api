from typing import Optional

from pydantic import BaseModel


class Portfolio(BaseModel):

    work_experience: Optional[int]
    github_link: Optional[str]
    linkedin_link: Optional[str]
    hh_link: Optional[str]


class CreatePortfolio(BaseModel):
    portfolio: Portfolio
    program_lang: list
    database: list
    knowledge_field: list


class GetPortfolio(BaseModel):
    kr: int
    user_id: int
    database_id: str
    knowledge_field_id: str
    program_lang_id: str


class EditPortfolio(CreatePortfolio):
    portfolio_id: int
