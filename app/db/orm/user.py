from sqlalchemy import (
    Column, String, Integer, )

from ._base import _Base


class User(_Base):
    idx = Column(
        Integer,
        primary_key=True,
        comment="primary key"
    )
    name = Column(
        String(120),
        nullable=False,
        index=True,
    )
    desc = Column(
        String(255),
    )


