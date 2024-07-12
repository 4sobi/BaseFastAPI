from typing import Optional

from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    idx: Optional[int] = None
    name: str
    desc: Optional[str] = None
