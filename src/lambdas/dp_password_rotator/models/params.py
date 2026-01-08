from pydantic import BaseModel


class RequestParams(BaseModel):
    e2e_user: str
    dp_account_id: str
