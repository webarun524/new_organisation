from pydantic import BaseModel


class RequestParams(BaseModel):
    environment: str
