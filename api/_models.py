from sqlalchemy import Boolean, Integer, String, Column
from ._database import Base, engine

class Todos(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String,nullable=False)
    description = Column(String,nullable=False)
    completed= Column(Boolean, default=False)

def table_create():
    Base.metadata.create_all(bind=engine)