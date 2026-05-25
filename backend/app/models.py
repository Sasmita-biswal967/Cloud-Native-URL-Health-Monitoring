from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float

from .database import Base


class Monitor(Base):
    __tablename__ = "monitors"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True)
    status = Column(String)
    status_code = Column(Integer)
    response_time = Column(Float)