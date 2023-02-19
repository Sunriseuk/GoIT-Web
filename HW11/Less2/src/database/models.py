from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from HW11.Less2.src.database.connect import Base


class Owner(Base):
    __tablename__ = "owners"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)


class Cat(Base):
    __tablename__ = "cats"

    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String, index=True)
    description = Column(String, index=True)
    age = Column(Integer)
    vaccinated = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("owners.id"), nullable=True)
    owner = relationship("Owner", backref="cats")
