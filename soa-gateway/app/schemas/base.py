from pydantic import BaseModel


class ErrorBase(BaseModel):
    error: str
