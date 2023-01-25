from sqlalchemy import Column, Integer, String, UniqueConstraint

from app.common.db import Base


class Value(Base):
    __tablename__ = 'values'

    value_id = Column(Integer, primary_key=True, nullable=False)
    value = Column(String, nullable=False)

    UniqueConstraint(value, name="value_constr")

    def __init__(self, *args, **kwargs):
        super(Value, self).__init__(*args, **kwargs)
