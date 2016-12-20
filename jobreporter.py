import bs4
import datetime
import requests
import pushbullet


class JobReport(object):

    def __init__(self, site_url, search_url, soup_param, db_session, db_model):
        self.site_url = site_url
        self.search_url = search_url
        self.soup_param = soup_param
        self.db_session = db_session
        self.db_model = db_model
        self.job_results = []
        self.final_results = []
        self.bullet_results = []

    def parse_results(self):
        """Method extracts job links and titles from job posting site"""

        html = requests.get(self.search_url).text
        soup = bs4.BeautifulSoup(html, "html.parser")
        first_element = self.soup_param["element_1"]
        first_class = self.soup_param["class_1"]
        first_id = self.soup_param["id_1"]
        second_element = self.soup_param["element_2"]
        second_class = self.soup_param["class_2"]
        title_position = self.soup_param["title_position"]

        if first_class is not None:
            rows = soup.find(first_element, first_class).find_all(second_element, second_class)
        else:
            rows = soup.find(first_element, id=first_id).find_all(second_element, second_class)

        for row in rows:
            if row.a is not None:
                job_link = self.site_url + row.a["href"]
                job_title = row.find_all("a")[title_position].get_text().strip("\n").split("\n")[0]
                self.job_results.append({"job_link": job_link, "job_title": job_title})

    def extract_jobs(self):
        """Method extracts non duplicate jobs by comparing job stored in the database"""

        link_query = self.db_session.query(self.db_model.job_link).all()

        for job in self.job_results:
            in_db = False
            for link in link_query:
                if link[0] == job["job_link"]:
                    in_db = True
            if not in_db:
                self.final_results.append(job)
                self.bullet_results.append({job["job_title"]: job["job_link"]})

    def write_results(self):
        """Method writes non duplicate results to the database"""

        for job in reversed(self.final_results):
            self.db_session.add(self.db_model(job_link=job["job_link"], job_title=job["job_title"]))

        self.db_session.commit()

    def delete_results(self):
        """Method deletes job postings older than 30 days from the database"""

        time_frame = datetime.date.today() - datetime.timedelta(days=-31)
        date_query = self.db_session.query(self.db_model).filter(self.db_model.date_created >= time_frame)
        date_query.delete(synchronize_session=False)

    def create_report(self, api, msg_tittle):
        """Method creates the report and sends a message of the new jobs postings."""

        self.parse_results()
        self.extract_jobs()
        self.write_results()
        self.delete_results()

        if self.bullet_results:
            pb = pushbullet.PushBullet(api)
            msg_body = "{0}".format(self.bullet_results)
            pb.push_note(msg_tittle, msg_body)
