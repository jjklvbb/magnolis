from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, backref

from app.common.db import Base


class MainTable(Base):
    __tablename__ = 'maintable'

    main_id = Column(Integer, primary_key=True, nullable=False)

    main_doc = Column(Integer, ForeignKey("textdocs.doc_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    doc = relationship("TextDoc", backref=backref("main_docs", cascade="all, delete"))

    main_attr = Column(Integer, ForeignKey("attributes.attr_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    attr = relationship("Attribute", backref=backref("main_attrs", cascade="all, delete"))

    main_value = Column(Integer, ForeignKey("values.value_id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    value = relationship("Value", backref=backref("main_values", cascade="all, delete"))

    UniqueConstraint(main_doc, main_attr, main_value, name="trio_constr")
    UniqueConstraint(main_doc, main_attr, name="duo3_constr")

    def __init__(self, *args, **kwargs):
        super(MainTable, self).__init__(*args, **kwargs)
