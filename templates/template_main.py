import logging.config
import json
from job import template_models
from job.jobreporter import JobReport
from sqlalchemy.orm import sessionmaker



# Enter PushBullet API key
PB_API = ""
# Enter the full path of the log config file
LOG_FILE = ""


with open(LOG_FILE, "rt") as file:
    config = json.load(file)
 
logging.config.dictConfig(config)
logger = logging.getLogger(__name__)


def main():

    Session = sessionmaker(bind=template_models.engine)
    session = Session()

    jr = JobReport(session, template_models.Job)

    craigslist_search(jr)
    jr.delete_results()
    logger.info("Tasks Complete!")


def craigslist_search(report):
    """
    Function scrapes job links from craigslist and sends a text message if there
    are new job postings not stored in the database.
    """

    msg_tittle = "Craiglist Jobs"
    # Site url used to create the job links
    site_url = "https://austin.craigslist.org"
    # Site url to parse job postings
    search_url = "https://austin.craigslist.org/search/sof"
    # Arguments used by bs4 to scrape job postings
    # See example section on the README.MD for a visual example
    soup_args = {"element_1": "ul", "class_1": "rows", "id_1": None, "element_2": "p",
                 "class_2": "result-info", "title_position": 0}

    report.create_report(API, msg_tittle, site_url, search_url, soup_args)


try:
    main()
except Exception:
    logger.error("craigslist_search error", exc_info=True)
