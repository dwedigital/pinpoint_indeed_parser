from indeed import IndeedFeed

brands = [
    "eyehear",
    "barretBarrett's Technology Solutionsts",
    "Island Stone",
    "sennsa",
    "Blacksheep Engineering",
    "systems design co",
    "Illusive Automation",
]

id = IndeedFeed()

jobs = []

for brand in brands:
    brand_jobs = id.find_client_jobs(brand, fuzzy_search=True)
    for job in brand_jobs:
        job["Indeed_Company"] = brand
    jobs.extend(brand_jobs)

# write jobs to CSV

import csv

with open("jobs.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=jobs[0].keys())
    writer.writeheader()
    for job in jobs:
        writer.writerow(job)
