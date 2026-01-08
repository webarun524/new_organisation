from pydantic import BaseModel


class RequestParams(BaseModel):
    execution_id: str
