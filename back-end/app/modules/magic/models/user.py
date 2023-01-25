from sqlalchemy import Column, Integer, String
from sqlalchemy import UniqueConstraint

from app.common.db import Base


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, nullable=False)
    login = Column(String, nullable=False)
    password = Column(String, nullable=False)
    UniqueConstraint(login, name="login_constr")

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
