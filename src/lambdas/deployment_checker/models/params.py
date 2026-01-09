from pydantic import BaseModel, Field

UUID_IN_BRACES_PATTERN = (
    r"^\{[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\}$"
)


class RequestParams(BaseModel):
    execution_uuid: str = Field(
        pattern=UUID_IN_BRACES_PATTERN, min_length=38, max_length=38
    )
