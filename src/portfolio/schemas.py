import datetime
from typing import Optional

from pydantic import BaseModel


class Portfolio(BaseModel):

    work_experience: Optional[int]
    knowledge_field: Optional[int]
    github_link: Optional[str]
    linkedin_link: Optional[str]
    hh_link: Optional[str]
    work_schedule: Optional[int]
