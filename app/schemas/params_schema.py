from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    skip: int = Field(ge=0, default=0)
    limit: int = Field(ge=1, le=100, default=100)