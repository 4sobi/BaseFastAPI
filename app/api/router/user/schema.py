from typing import Optional

from pydantic import BaseModel

from db import model


class CreateUserRequest(BaseModel):
    name: str
    desc: Optional[str] = None


