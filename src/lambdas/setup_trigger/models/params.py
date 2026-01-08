from pydantic import BaseModel


class RequestParams(BaseModel):
    environment: str
    bb_env_code: str
    target_branch_name: str
