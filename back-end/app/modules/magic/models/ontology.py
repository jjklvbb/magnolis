from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship, backref

from app.common.db import Base


class Ontology(Base):
    __tablename__ = 'ontologies'

    ont_id = Column(Integer, primary_key=True, nullable=False)
    ont_name = Column(String, nullable=False)
    ont_owner = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    user = relationship("User", backref=backref("onts", cascade="all, delete"))

    attr_entity_name = Column(String, nullable=False)
    attr_date = Column(String, nullable=False)

    UniqueConstraint(ont_name, ont_owner, name="name_constr")

    def __init__(self, *args, **kwargs):
        super(Ontology, self).__init__(*args, **kwargs)
