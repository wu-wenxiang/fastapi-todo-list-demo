from typing import Type

from sqlalchemy import TIMESTAMP, Column, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base

Base: Type = declarative_base()


class Todoelem(Base):
    __tablename__ = "todoelem"

    id = Column(Integer, primary_key=True, comment="id primary key")
    name = Column(String(200), nullable=True, comment="name")
    description = Column(String(2000), nullable=True, comment="description")
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, onupdate=text("CURRENT_TIMESTAMP"))

    def __repr__(self):
        return self.name

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
