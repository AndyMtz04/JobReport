import json

import csv

import os

from datetime import datetime

from urllib.request import urlopen

from bs4 import BeautifulSoup

from pushbullet import PushBullet


class JobReport(object):

    def __init__(self, file_name, file_path):
        self.file_name = file_name
        self.file_path = file_path
        self.complete_path = self.file_path + self.file_name

    def parse_results(self, url):
        """Function parses job postings from a cragslist job section.
        """
        results = []
        count = 0
        html = urlopen(url).read()
        soup = BeautifulSoup(html, "html.parser")
        rows = soup.find("div", "content").find_all("p", "row")
        for row in rows:
            if count < 30:
                count += 1
                job_url = "https://austin.craigslist.org" + row.a["href"]
                job_date = row.find("time").get("datetime")
                job_title = row.find_all("a")[1].get_text()
                results.append({"job_url": job_url, "job_date": job_date,
                                "job_title": job_title})
            else:
                break
        return results

    def austincc_parse(self, url):
        """Function parses job data into a list from
        http://sites.austincc.edu/ with import.io's api.
        """
        results = []
        html = urlopen(url)
        content = html.read().decode(html.headers.get_content_charset())
        json_dict = json.loads(content)
        if "ehire" in json_dict["pageUrl"]:
            for x in json_dict["results"]:
                job_title = x["title_link/_text"]
                job_url = x["jobnumber_link"]
                job_location = x["location_value"]
                results.append({"job_title": job_title, "job_url": job_url,
                                "job_location": job_location})
        else:
            for x in json_dict["results"]:
                job_title = x["linemajor_link/_text"]
                job_url = x["linemajor_link"]
                job_time = x["subsmall_value_2"]
                job_company = x["subsmall_value_1"]
                results.append({"job_title": job_title, "job_url": job_url,
                                "job_time": job_time,
                                "job_company": job_company})
        return results

    def indeed_parse(self, url):
        """Function parses job data into a list from
        indeed.com with import.io's api.
        """
        results = []
        html = urlopen(url)
        content = html.read().decode(html.headers.get_content_charset())
        json_dict = json.loads(content)
        for x in json_dict["results"]:
            job_title = x["turnstilelink_link_1/_title"]
            job_url = x["turnstilelink_link_1"]
            results.append({"job_title": job_title, "job_url": job_url})
        return results

    def write_results(self, results):
        """Function writes results to a specified csv file"""
        fields = list(results[0].keys())
        with open(self.complete_path, "w") as file:
            dw = csv.DictWriter(file, fieldnames=fields, delimiter="|",
                                lineterminator="\n")
            dw.writer.writerow(dw.fieldnames)
            dw.writerows(results)

    def has_new_records(self, results):
        """Function compares results with stored results to determine
         if new jobs have been posted.
         """
        current_posts = [x["job_url"] for x in results]
        if not os.path.exists(self.complete_path):
            with open(self.complete_path, "w") as new_file:
                return True
        with open(self.complete_path, "r") as file:
            reader = csv.DictReader(file, delimiter="|")
            seen_posts = [row["job_url"] for row in reader]

        is_new = False
        for post in current_posts:
            if post in seen_posts:
                pass
            else:
                is_new = True
        return is_new

    def send_bullet(self, api, title, msg):
        """Function sends text message to specified recipient using
        pushbullet.
        """
        pb = PushBullet(api)
        pb.push_note(title, msg)

    def get_current_time(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def extract_job(self, results):
        """Function extracts new job titles and urls from results."""
        final_results = []
        with open(self.complete_path, "r") as file:
            reader = csv.DictReader(file, delimiter="|")
            seen_results = [x for x in reader]
            for x in range(len(results)):
                if results[x] in seen_results:
                    pass
                else:
                    job_title = results[x]["job_title"]
                    job_url = results[x]["job_url"]
                    final_results.append({job_title: job_url})
        return final_results
