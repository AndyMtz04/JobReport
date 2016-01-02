import json

import csv

import os

import smtplib

from datetime import datetime

from urllib.request import urlopen

from bs4 import BeautifulSoup


class JobReport(object):

    def __init__(self, file_name, file_path):
        self.file_name = file_name
        self.file_path = file_path
        self.complete_path = self.file_path + self.file_name

    def parse_results(self, url):
        """Function parses job postings from a cragslist job section."""
        results = []
        count = 0
        html = urlopen(url).read()
        soup = BeautifulSoup(html, "html.parser")
        rows = soup.find("div", "content").find_all("p", "row")
        for row in rows:
            if count < 30:
                count += 1
                post_url = "https://austin.craigslist.org" + row.a["href"]
                post_date = row.find("time").get("datetime")
                post_title = row.find_all("a")[1].get_text()
                results.append({"url": post_url, "post_date": post_date,
                                "post_title": post_title})
            else:
                break
        return results

    def austincc_parse(self, url):
        """Function parses job data into a list from
        http://sites.austincc.edu/jobs/jobs with import.io's api.
        """
        results = []
        html = urlopen(url)
        content = html.read().decode(html.headers.get_content_charset())
        dict = json.loads(content)
        for x in dict["results"]:
            job_title = x["linemajor_link/_text"]
            job_link = x["linemajor_link"]
            job_time = x["subsmall_value_2"]
            job_company = x["subsmall_value_1"]
            results.append({"job_title": job_title, "job_link": job_link,
                            "job_time": job_time, "job_company": job_company})
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
        current_posts = [x["url"] for x in results]
        if not os.path.exists(self.complete_path):
            with open(self.complete_path, "w") as new_file:
                return True
        with open(self.complete_path, "r") as file:
            reader = csv.DictReader(file, delimiter="|")
            seen_posts = [row["url"] for row in reader]

        is_new = False
        for post in current_posts:
            if post in seen_posts:
                pass
            else:
                is_new = True
        return is_new

    def send_text(self, username, password, phone_number, msg):
        """Function sends text message to specified recipient using
        gmail.
        """
        from_address = "Craigslist Checker"
        to_address = phone_number + "@tmomail.net"
        msg = "From: {0}\r\nTo: {1}\r\n\r\n{2}".format(from_address,
                                                       to_address, msg)
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(username, password)
        server.sendmail(from_address, to_address, msg)
        server.quit()

    def get_current_time(self):
        return datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")

    def new_job(self, results):
        """Function extracts new job titles and urls from results."""
        final_results = []
        with open(self.complete_path, "r") as file:
            reader = csv.DictReader(file, delimiter="|")
            seen_results = [x for x in reader]
            for x in range(len(results)):
                if results[x] in seen_results:
                    pass
                else:
                    post_title = results[x]["post_title"]
                    post_url = results[x]["url"]
                    final_results.append({post_title: post_url})
        return final_results
