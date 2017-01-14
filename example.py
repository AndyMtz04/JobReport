import datetime
import logging.config
import json
from jobreporter import JobReport
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker

# Enter PushBullet API
API = ""

# This example uses postgresql database.
# Enter correct password and database name to connect
engine = create_engine('postgresql://postgres:password1@localhost/db_name', echo=False)
Base = declarative_base()

# Model used to created the database columns
class Job(Base):

    __tablename__ = "Jobs"

    id = Column(Integer, primary_key=True)
    job_title = Column(String)
    job_link = Column(String)
    date_created = Column(Date, default=datetime.date.today())

Base.metadata.create_all(engine)


def main():

    with open("logging.json", "rt") as file:
        config = json.load(file)

    logging.config.dictConfig(config)
    logger = logging.getLogger(__name__)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        craigslist_search(session)
    except Exception:
        logger.error("craigslist_search error", exc_info=True)


def craigslist_search(session):
    """
    Function scrapes job links from craigslist and sends a text message if there
    are new job postings not stored in the database.
    """

    # Site url used to create the job links
    site_url = "https://austin.craigslist.org"
    # Site url to parse job postings
    search_url = "https://austin.craigslist.org/search/sof"
    # Arguments used by bs4 to scrape job postings
    # See example section on the README.MD for a visual example
    soup_args = {"element_1": "ul", "class_1": "rows", "id_1": None, "element_2": "p",
                 "class_2": "result-info", "title_position": 0}
    msg_tittle = "Craiglist Jobs"

    jr = JobReport(site_url, search_url, soup_args, session, Job)

    jr.create_report(API, msg_tittle)