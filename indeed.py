import requests
from lxml import etree
from datetime import datetime
import glob
import os
from dotenv import load_dotenv

load_dotenv()


class IndeedFeed:
    def __init__(self, test=False):

        self.url = os.getenv("INDEED_FEED_URL")
        self.test_file_path = "mock_indeed_feed.xml"
        self.test = test

    def write_feed(self):
        if self.__need_new_feed():
            self.__clean_up_files()

            response = requests.get(self.url, stream=True)
            current_time = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")

            with open(f"indeed_feed_{current_time}.xml", "wb") as f:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    f.write(chunk)
        else:
            return

    def find_client_jobs(self, client_name=None, fuzzy_search=False) -> list:
        jobs = []
        # Parse the XML file and find jobs for the client

        root = self.__parse_xml()
        for job in root.iter("job"):

            if fuzzy_search:
                if client_name.lower() in job.find("company").text.lower():
                    jobs.append(
                        {
                            "Company": job.find("company").text,
                            "Job Reference": job.find("referencenumber").text,
                            "Job Title": job.find("title").text,
                        }
                    )

            else:
                if client_name.lower() == job.find("company").text.lower():
                    jobs.append(
                        {
                            "Job Reference": job.find("referencenumber").text,
                            "Job Title": job.find("title").text,
                        }
                    )

        return jobs

    def find_job_by_reference(self, reference) -> dict:
        # Parse the XML file and find job by reference
        root = self.__parse_xml()
        for job in root.iter("job"):
            if reference in job.find("referencenumber").text:
                return {
                    "Job Reference": job.find("referencenumber").text,
                    "Job Title": job.find("title").text,
                }
        return {"message": "Job not found"}

    def feed_stats(self):

        root = self.__parse_xml()
        jobs = root.findall("job")
        return {
            "Total Jobs": len(jobs),
            "Number of clients": len(set([job.find("company").text for job in jobs])),
        }

    def __parse_xml(self):
        if self.test:
            tree = etree.parse(self.test_file_path)
            root = tree.getroot()
            return root

        else:
            # Find the file with the latest date
            files = glob.glob("indeed_feed_*.xml")
            if files:
                latest_file = max(files, key=os.path.getctime)
            else:
                self.write_feed()
                files = glob.glob("indeed_feed_*.xml")
                latest_file = max(files, key=os.path.getctime)
            tree = etree.parse(latest_file)
            root = tree.getroot()
            return root

    def __clean_up_files(self):
        # get an array of any files with the following format: indeed_feed_*.xml
        files = glob.glob("indeed_feed_*.xml")
        # remove any files that match the format
        if files:
            for file in files:
                os.remove(file)

    def __need_new_feed(self):
        # if the file is older than 1 hour, return true
        files = glob.glob("indeed_feed_*.xml")
        if files:
            latest_file = max(files, key=os.path.getctime)
            time_difference = datetime.now() - datetime.fromtimestamp(
                os.path.getctime(latest_file)
            )
            if time_difference.total_seconds() > 3600:
                return True
        elif not files:
            return True
        return False
