import re
from datetime import datetime

from sqlalchemy import Column, DateTime, MetaData
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import declarative_base

metadata = MetaData()


metadata = MetaData()

# 기본 클래스 생성
Base = declarative_base(metadata=metadata)


class _Base(Base):
    __abstract__ = True

    created_at = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
        index=True,
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    @declared_attr
    def __tablename__(cls) -> str:
        table_name = re.sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__).lower()
        return f'tbl_{table_name}'
