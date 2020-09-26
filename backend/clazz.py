from pydantic import BaseModel


class loginValid(BaseModel):
    enc: str
    uuid: str
    session: dict
