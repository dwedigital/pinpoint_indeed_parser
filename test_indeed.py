import unittest
from indeed import IndeedFeed
import glob
import os
from lxml import etree

class TestIndeed(unittest.TestCase):

    # Test the request for the feed and file creation first
    def test_write_and_parse_feed(self):
        indeedFeed = IndeedFeed()
        indeedFeed.write_feed()

        self.assertTrue(self.__feed_exists())

        root = indeedFeed._IndeedFeed__parse_xml()

        self.assertIsInstance(root, etree._Element, "Root is not an ElementTree object")
        self.assertEqual(
            root.find("publisher").text, "Pinpoint", "Publisher is not Pinpoint"
        )

    # use mock feed xml to test feed_stats method
    def test_feed_stats(self):
        indeedFeed = IndeedFeed(test=True)
        stats = indeedFeed.feed_stats()
        self.assertEqual(stats, {"Total Jobs": 13396, "Number of clients": 1205})

    # test the find_job_by_reference method
    def test_find_job_by_reference(self):
        indeedFeed = IndeedFeed(test=True)
        job = indeedFeed.find_job_by_reference("8330")
        self.assertEqual(
            job,
            {"Job Reference": "8330", "Job Title": "Education Consultant - Nigeria"},
        )

    def test_find_client_jobs(self):
        indeedFeed = IndeedFeed(test=True)
        jobs = indeedFeed.find_client_jobs("Continuum", True)
        self.assertEqual(
            jobs,
            [
                {
                    "Company": "Continuum",
                    "Job Reference": "11810",
                    "Job Title": "Bursary Programme",
                },
                {
                    "Company": "Continuum",
                    "Job Reference": "18005",
                    "Job Title": "Analyst",
                },
            ],
        )

    def __feed_exists(self):
        files = glob.glob("indeed_feed_*.xml")
        if files:
            return True
        else:
            return False
        

    # Teardown the file creation clean up
    @classmethod
    def tearDownClass(self):
        for file in glob.glob("indeed_feed_*.xml"):
            os.remove(file)


if __name__ == "__main__":
    unittest.main()
