from jobreporter import JobReport

FILE_PATH = ""
API = "" # pushbullet api key


def main():

    tech_url = "https://austin.craigslist.org/search/tch"

    search_jobs(tech_url, "tech_support.csv")


def search_jobs(url, file_name):
    """Function uses the jobreporter class to start
    searching for jobs and determines which parser to use.
    """
    job = JobReport(file_name, FILE_PATH)
    job_type = file_name.replace(".csv", "")
    if "craigslist" in url:
        results = job.parse_results(url)
        if job.has_new_records(results):
            message = "{0}".format(job.extract_job(results))
            job.send_bullet(API, job_type, message)
            job.write_results(results)
        else:
            #print("{0} no new jobs for {1}".format(job.get_current_time(),
                                                   #job_type))
            pass

    elif "austincc" in url:
        results = job.austincc_parse(url)
        if job.has_new_records(results):
            message = "{0}".format(job.extract_job(results))
            job.send_bullet(API, job_type, message)
            job.write_results(results)
        else:
            #print("{0} no new jobs for {1}".format(job.get_current_time(),
                                                   #job_type))
            pass

    else:
        results = job.indeed_parse(url)
        if job.has_new_records(results):
            message = "{0}".format(job.extract_job(results))
            job.send_bullet(API, job_type, message)
            job.write_results(results)
        else:
            #print("{0} no new jobs for {1}".format(job.get_current_time(),
                                                   #job_type))
            pass

main()
