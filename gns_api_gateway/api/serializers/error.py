from pydantic import BaseModel

__all__ = ["ErrorModel"]


class ErrorModel(BaseModel):
    code: str
    message: str
