import datetime
from jobreporter import JobReport
from pushbullet import PushBullet
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

    pb = PushBullet(API)
    Session = sessionmaker(bind=engine)
    session = Session()

    craigslist_search(session, pb)


def craigslist_search(session, pb):
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

    jr = JobReport(site_url, search_url, soup_args, session, Job)
    jr.parse_results()
    jr.extract_jobs()
    jr.write_results()
    jr.delete_results()

    # PushBullet message will be sent if there are new postings
    if jr.bullet_results:
        tittle = "Craigslist Jobs"
        message = "{0}".format(jr.bullet_results)
        pb.push_note(tittle, message)