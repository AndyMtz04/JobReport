import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date

# Enter the database uri to connect to the database
engine = create_engine('<enter db uri here>', echo=False)
Base = declarative_base()


class Job(Base):

    __tablename__ = "Jobs"

    id = Column(Integer, primary_key=True)
    job_title = Column(String)
    job_link = Column(String)
    date_created = Column(Date, default=datetime.date.today())

Base.metadata.create_all(engine)
