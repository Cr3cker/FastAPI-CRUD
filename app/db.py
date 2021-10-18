from datetime import datetime
from sqlalchemy.orm import declarative_base
import databases
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, create_engine

DATABASE_URL = "postgresql+psycopg2://postgres:1111@localhost/sqlalchemy_tuts"

Base = declarative_base()

engine = create_engine(DATABASE_URL, echo=False)


class Posts(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(200))
    content = Column(Text, nullable=False)
    published = Column(Boolean, default=False, nullable=False)
    created_on = Column(DateTime, default=datetime.now())
    updated_on = Column(DateTime, default=datetime.now())


database = databases.Database(DATABASE_URL)
