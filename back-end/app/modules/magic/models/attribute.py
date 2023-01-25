from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, backref

from app.common.db import Base


class Attribute(Base):
    __tablename__ = 'attributes'

    attr_id = Column(Integer, primary_key=True, nullable=False)
    attr_name = Column(String, nullable=False)

    attr_ont = Column(Integer, ForeignKey("ontologies.ont_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    ont = relationship("Ontology", backref=backref("attrs", cascade="all, delete"))

    UniqueConstraint(attr_name, attr_ont, name="duo2_constr")

    def __init__(self, *args, **kwargs):
        super(Attribute, self).__init__(*args, **kwargs)
