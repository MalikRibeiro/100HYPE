
from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr

@as_declarative()
class Base:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

# Import all models here for Alembic
from app.models.user import User  # noqa
from app.models.asset import Asset  # noqa
from app.models.transaction import Transaction  # noqa
from app.models.analysis import AIAnalysis  # noqa
