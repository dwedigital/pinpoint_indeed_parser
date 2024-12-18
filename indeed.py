"""Main module used for separating the IndeedFeed class logic from any script or CLI that uses it."""

from datetime import datetime
import glob
import os
import xml.etree.ElementTree as etree

import requests

from dotenv import load_dotenv
from progress.spinner import PixelSpinner

load_dotenv()


class IndeedFeed:
    """This class is responsible for downloading the Indeed feed and parsing it to find jobs for a specific client."""

    def __init__(self, test=False):
        """Sets up the class with the necessary variables and calls the write_feed method."""
        self.url = os.getenv("INDEED_FEED_URL")
        self.test_file_path = "mock_indeed_feed.xml"
        self.test = test
        self.write_feed()

    def write_feed(self):
        """The main function that handles logic for whether to download a new feed or not."""
        if self.__need_new_feed():
            with PixelSpinner("Processing XML    ") as spinner:
                self.__clean_up_files()
                response = requests.get(self.url, stream=True, timeout=20)
                current_time = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")

                with open(f"indeed_feed_{current_time}.xml", "wb") as f:
                    for chunk in response.iter_content(chunk_size=1024 * 1024):
                        f.write(chunk)
                        spinner.next()

    def find_client_or_source_jobs(
        self, client_name=None, fuzzy_search=False, source_name=False
    ) -> list:
        """Method to find jobs based on client name or source name.

        Args:
            client_name (_type_, optional): _description_. Defaults to None.
            fuzzy_search (bool, optional): _description_. Defaults to False.
            source_name (bool, optional): _description_. Defaults to False.

        Returns:
            list: list of jobs
        """
        jobs = []

        # Parse the XML file and find jobs for the client
        root = self.__parse_xml()
        for job in root.iter("job"):
            if fuzzy_search:
                # Search by source name
                if source_name:
                    if (
                        client_name.lower() in job.find("sourcename").text.lower()
                        or client_name.lower()
                        in job.find("sourcename").text.lower().replace(" ", "")
                        or client_name.lower().replace(" ", "")
                        in job.find("sourcename").text.lower()
                    ):
                        jobs.append(self.__pluck_simple(job))

                # Search by company name
                else:
                    if (
                        client_name.lower() in job.find("company").text.lower()
                        or client_name.lower()
                        in job.find("company").text.lower().replace(" ", "")
                        or client_name.lower().replace(" ", "")
                        in job.find("company").text.lower()
                    ):
                        jobs.append(self.__pluck_simple(job))

            else:
                # Use exact match in searching (still case insensitive)
                if source_name:
                    if client_name.lower() == job.find("sourcename").text.lower():
                        jobs.append(self.__pluck_simple(job))

                    if client_name.lower() == job.find("company").text.lower():
                        jobs.append(self.__pluck_simple(job))

        return jobs

    def find_job_by_reference(self, reference) -> dict:
        """Searches for a job by reference number.

        Args:
            reference (_type_): _description_

        Returns:
            dict: _description_
        """
        root = self.__parse_xml()
        for job in root.iter("job"):
            if reference in job.find("referencenumber").text:
                print("found")

                return self.__pluck_full(job)

        return {"message": "Job not found"}

    def feed_stats(self):
        """Returns the total number of jobs and the number of clients.

        Returns:
            _type_: _description_
        """
        root = self.__parse_xml()
        jobs = root.findall("job")
        return {
            "Total Jobs": len(jobs),
            "Number of clients/brands": len({job.find("company").text for job in jobs}),
            "Number of sources": len({job.find("sourcename").text for job in jobs}),
        }

    def __parse_xml(self):
        if self.test:
            tree = etree.parse(self.test_file_path)
            root = tree.getroot()
            return root
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

    def __pluck_simple(self, job: etree.Element) -> dict:
        return {
            "Source": (
                job.find("sourcename").text
                if job.find("sourcename") is not None
                else ""
            ),
            "Company": (
                job.find("company").text if job.find("company") is not None else ""
            ),
            "Job Reference": (
                job.find("referencenumber").text
                if job.find("referencenumber") is not None
                else ""
            ),
            "Job Title": (
                job.find("title").text if job.find("title") is not None else ""
            ),
        }

    def __pluck_full(self, job) -> dict:
        return {
            "Company": (
                job.find("company").text if job.find("company") is not None else ""
            ),
            "Job Reference": (
                job.find("referencenumber").text
                if job.find("referencenumber") is not None
                else ""
            ),
            "Job Title": (
                job.find("title").text if job.find("title") is not None else ""
            ),
            "Salary": (
                job.find("salary").text if job.find("salary") is not None else ""
            ),
            "Job Description": (
                job.find("description").text
                if job.find("description") is not None
                else ""
            ),
            "Email": (job.find("email").text if job.find("email") is not None else ""),
            "Apply Data": (
                job.find("indeed-apply-data").text
                if job.find("indeed-apply-data") is not None
                else ""
            ),
        }
