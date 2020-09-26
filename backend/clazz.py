from pydantic import BaseModel


class Valid(BaseModel):
    enc: str
    uuid: str
    session: dict
