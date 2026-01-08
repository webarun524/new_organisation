from typing import Optional

from pydantic import BaseModel


class ParamsModel(BaseModel):
    Id: str
    IsSuccess: bool
    ErrorDetails: Optional[str] = None
