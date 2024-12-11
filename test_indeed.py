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
        print(job)
        self.assertEqual(
            job,
            {
                "Company": "The Christian Reformed Church in North America",
                "Job Reference": "8330",
                "Job Title": "Education Consultant - Nigeria",
                "Salary": "",
                "Job Description": '<h3>Description</h3><br><div>\n<strong>PURPOSE/OVERVIEW:<br></strong>Resonate Global Mission of the Christian Reformed Church in North America (CRCNA), has a full-time opening for an Education Consultant for West Africa. The Anglophone West Africa Education Consultant is responsible to facilitate the development, strengthening and improvement of primary through secondary level Christian education throughout Nigeria and other Anglophone West African countries.</div><div>\xa0<br>This position will remain open until filled.<strong><br></strong><br>\n</div><br><h3>KEY RESPONSIBILITIES:</h3><br><div><strong>Essential Duties and Responsibilities</strong></div><div>1. Dialogue with Christian schools throughout Anglophone West Africa, both directly and through associations of Christian schools.<br>\xa02. Mentor and encourage key leaders in the Christian school movement.<br>\xa03. Assess teaching materials and methods used in Anglophone West African schools and integrate the best of these into the development of Christian school curriculum.<br>\xa04. Participate in the training of teachers to integrate a Biblical worldview into their teaching.<br>\xa05. Participate in the training of Christian school administrators to competently administer their schools.<br>\xa06. Interact and collaborate with other Resonate missionaries involved in education in West Africa.<br>\xa07. Encourage and coordinate the involvement of other organizations in Christian school development in Anglophone West Africa, especially other CRCNA-related agencies.<br>\xa08. Participate in African and worldwide discussions of Christian education.<br>\xa09. Identify and develop strategic ministry opportunities for short-term volunteers that utilize the skills and strengths of the CRCNA in the development of Christian education.<br>\xa010. Work with country team leaders in the orientation, mentoring and supervision of volunteers while they are in West Africa.<br>\xa011. Participate in support-raising (e.g., prayer, care and financial support) for Resonate ministries by developing and maintaining a network of supporting churches and individuals.<br>\xa012. Ensure notes of thanks are sent to donors in a timely manner.<br>\xa013. Educate the CRCNA and others about the nature of the global church and its mission, encouraging them to develop a deeper passion and involvement in global missions.<br>\xa014. Provide the CRCNA with insight and resources for ministry among minority racial/national/religious groups living in North America about which the missionary has knowledge and expertise.<br>\xa015. Communicate the nature and value of Resonate’s ministries to the CRCNA and others through written communications, and through preaching/speaking engagements.</div><div><br></div><div>\n<strong>Supervisory Responsibilities<br></strong>None</div><br><h3>SKILLS, KNOWLEDGE & EXPERTISE:</h3><br><div><strong>Qualifications</strong></div><div>1. Professing membership in a Christian Reformed congregation, or of a church in ecclesiastical fellowship with the CRCNA, and agreement with the doctrine of the church signified by signing a covenant statement.<br>\xa02. Demonstrated passion for Christian education.<br>\xa03. Demonstrated ability to work with others from different cultures and religious traditions.<br>\xa04. Demonstrated intercultural experience and competence.<br>\xa05. Self-motivated and proven quality administrative and organizational skills.<br>\xa06. Training and experience in cross-cultural ministry, preferably in an African context or in global missions.<br>\xa07. Fluency in English.\xa0</div><div>\n<strong><br>Education & Experience<br></strong><br>\n</div><ul>\n<li>Bachelor’s degree in Education or related field; Master’s degree in Education, or related field, preferred (completed or in progress).</li>\n<li>At least 3 years of experience in Christian Education (preferably in both classroom teaching and administration).\xa0</li>\n</ul><div>\xa0</div><div>\n<br><strong>*****INTERMEDIATE STEPS</strong><br> The successful candidate for this position will pass through two intermediate steps before taking up the tasks outlined in this position description; the rate range for each step is included.<br>\xa0<br>Step #1<br> Missionary Candidate: The purpose of this position is to prepare for international service by building a network of prayer, care and financial support in North America that will enable future ministry. Ordinarily, this will progress from part-time to full-time as the support network grows through the work of the candidate and the missionary support team that is designed for this purpose. One can expect to be in this role for 6 to 12 months, depending on how quickly the support network comes together. The pay range for this step is on the CRCNA Domestic scale.</div><div>\n<br>Step #2<br>\xa0Missionary in Training: The purpose of this role is to develop language and culture skills, ministry skills and relationships that will enable future ministry, and begin to use those in ministry. Ordinarily, one can expect to be in this role for 6 to 18 months, depending on prior background and experience. The pay range for this step is US or Canada on the CRCNA International scale.</div><div>\n<br><br><br>\n</div><br><h3>PHYSICAL DEMANDS & WORK ENVIRONMENT:</h3><br><div><strong>Physical Demands</strong></div><div>The physical demands described here are representative of those that must be met by an employee to successfully perform the essential functions of this job. Reasonable accommodations may be made to enable individuals with disabilities to perform the essential functions.<br>\xa0<br><strong>Work Environment<br></strong>The work environment characteristics described here are representative of those an employee encounters while performing the essential functions of this job.<br><br>Flexible and adaptable to African travel, communications, and living conditions. <br><br><strong><br>Application Instructions: </strong>Please upload your resume and cover letter as one .pdf or .doc/.docx file.</div><br><h3>About The Christian Reformed Church in North America</h3><div>\n<strong>Who We Are</strong><br><strong>The Christian Reformed Church in North America (CRCNA) includes just over one thousand congregations across the United States and Canada. About 75 percent of the churches are in the United States and 25 percent are in Canada. While we\'re a denomination with churches and ministries in two countries, we share in the blessings of ecclesial unity and joint ministry. Almost 230,000 people belong to the CRCNA—not a large number when you consider the population of our two countries. But by God’s grace we can accomplish a lot when we work together.<br><br></strong>The <a href="https://www.crcna.org/"><strong>CRCNA</strong></a> denominational offices serve the local church, providing resources to pastors and congregations so that people are introduced to Jesus Christ and their faith is nurtured. Other agencies of the CRCNA include <a href="https://reframeministries.org/"><strong>ReFrame Ministries</strong></a><strong>, </strong><a href="https://www.resonateglobalmission.org/"><strong>Resonate Global Mission</strong></a> and <a href="https://worldrenew.net/"><strong>World Renew</strong></a>.<br><br><strong>Be Who You Are</strong>\n</div><div>The CRCNA is committed to building a culture of belonging that encourages, supports, and celebrates the voices and experiences of all our employees. We strive to build a workforce that reflects the diversity of our broader culture and the Christian church, and invite all qualified candidates to apply.\xa0</div><div>\n<strong><br></strong><a href="https://docs.google.com/document/d/1NBCIPmiyMMOqYoavOTthM2J078Q1Zjd1ZOzTsoQi5B4/edit?usp=sharing"><strong>To read the CRCNA Diversity Statement click here</strong></a>\n</div>',
                "Email": "wbatchelder@crcna.org",
                "Apply Data": "",
            },
        )

    def test_find_client_or_source_jobs(self):
        indeedFeed = IndeedFeed(test=True)
        jobs = indeedFeed.find_client_or_source_jobs("Continuum", True)
        self.assertEqual(
            jobs,
            [
                {
                    "Source": "Continuum",
                    "Company": "Continuum",
                    "Job Reference": "11810",
                    "Job Title": "Bursary Programme",
                },
                {
                    "Source": "Continuum",
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
