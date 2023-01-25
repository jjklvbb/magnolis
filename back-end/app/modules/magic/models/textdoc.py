from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, backref

from app.common.db import Base


class TextDoc(Base):
    __tablename__ = 'textdocs'

    doc_id = Column(Integer, primary_key=True, nullable=False)
    doc_name = Column(String, nullable=False)
    doc_text = Column(String, nullable=True)

    # Документ (numdoc) привязан к онтологии (owner)
    doc_ont = Column(Integer, ForeignKey("ontologies.ont_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    ont = relationship("Ontology", backref=backref("textdocs", cascade="all, delete"))

    UniqueConstraint(doc_name, doc_ont, name="duo_constr")

    def __init__(self, *args, **kwargs):
        super(TextDoc, self).__init__(*args, **kwargs)
