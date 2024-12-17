"""
Simple script to find jobs for a list of client sub-brands and write them to a CSV file.
"""

import csv
from indeed import IndeedFeed

# Add the list of client sub-brands here
brands = []
# update the client name here for file naming
CLIENT_NAME = "client_name"

feed = IndeedFeed()

jobs = []

for brand in brands:
    brand_jobs = feed.find_client_or_source_jobs(brand, fuzzy_search=True)
    for job in brand_jobs:
        job["Indeed_Company"] = brand
    jobs.extend(brand_jobs)

# write jobs to CSV

with open(f"{CLIENT_NAME}.csv", "w", newline="", encoding=str) as f:
    writer = csv.DictWriter(f, fieldnames=jobs[0].keys())
    writer.writeheader()
    for job in jobs:
        writer.writerow(job)
