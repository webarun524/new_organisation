from pydantic import BaseModel

from shared.domain.type import OSDUVersion


class RequestParams(BaseModel):
    environment: str
    osdu_version: OSDUVersion
    bb_env_code: str
    bb_env_name: str
