from indeed import IndeedFeed
brands = [
'Acworth Animal Hospital',
"All Pets Hospital",
"American Veterinary Group",
"Angel Animal Hospital & Boarding",
"Animal Clinic of West Lake Worth",
"Animal General Hospital",
"Animal Health Center of Land O' Lakes",
"Animal Hospital of Montgomery",
"Animal Hospital of Peak Plaza",
"Animal Medical Center at St. Johns",
"Asheboro Animal Hospital",
"Atlas Pet Clinic",
"AVC",
"Azalea City Animal Hospital",
"Bainbridge Animal Hospital",
"Baldwin Animal Clinic",
"Bartow Animal Hospital",
"Baytree Animal Hospital",
"Bee Ridge Veterinary Clinic",
"Big Springs Veterinary Hospital",
"Bradford Animal Hospital",
"Branch's Veterinary Clinic - Nashville",
"Cairo Animal Hospital",
"Caldwell Animal Hospital",
"Care Animal Hospital",
"Cherryville Animal Hospital",
"Circle of Life Animal Hospital",
"Clanton-Malphus-Hodges Veterinary Hospital",
"Companion Animal Hospital",
"Compassion Animal Hospital",
"Cordova Station Animal Hospital",
"CountryChase Veterinary Hospital",
"Courtenay Animal Hospital",
"Crossroads Animal Hospital",
"Dadeland Animal Hospital",
"Daniels Parkway Animal Hospital",
"Dogwood Veterinary Hospital & Pet Resort",
"Dothan Animal Hospital",
"Durant Animal Hospital",
"Durham Veterinary Clinic",
"Dykes Veterinary Clinic",
"English Plaza Animal Hospital",
"Estero Animal Hospital",
"Forest Lakes Animal Clinic",
"Gulf Gate Animal Hospital",
"Gulfshore Animal Hospital",
"Haile Plantation Animal Hospital",
"Heart of Florida Animal Hospital & Pet Resort",
"Hillside Veterinary Hospital",
"Jensen Beach Animal Hospital",
"Kimbrough Animal Hospital",
"Lake City Animal Hospital (Florida)",
"Lake City Animal Hospital (Georgia)",
"Lake Hickory Veterinary Hospital",
"Lakeside Animal Hospital (Florida)",
"Lakeside Animal Hospital (North Carolina)",
"Leesburg Animal Hospital",
"Lighthouse Veterinary Clinic",
"Lincolnton Animal Hospital",
"Lindsey & Wills Animal Hospital",
"Lineberger Veterinary Hospital",
"Magnolia Animal Hospital",
"Mitchell Co. Animal Clinic",
"Navarre Animal Hospital",
"North Port St. Lucie Animal Hospital",
"Northside Animal Clinic",
"Oak Ridge Animal Clinic",
"Panhandle Veterinary Services",
"Parkway Animal Hospital",
"Pasquotank Animal Hospital",
"Pet Care Center",
"Piedmont Equine Associates",
"Pleasantburg Veterinary Clinic",
"Raleigh Community Animal Hospital",
"Riverside Animal Hospital",
"Rocky Creek Veterinary Hospital",
"Satilla Animal Hospital",
"Scotts Creek Animal Hospital",
"Shepherd Spring Animal Hospital",
"Small Animal Hospital",
"South Ocala Animal Clinic",
"South Point Pet Hospital",
"Southgate Animal Hospital",
"Southside Animal Hospital",
"Spring Hill Animal Clinic",
"Stuart Sound Animal Hospital",
"Suwannee Valley Veterinary Clinic",
"Town & Country Veterinarians",
"Upper Keys Veterinary Hospital",
"UrgentVet",
"Village Animal Clinic",
"West Boca Veterinary Center",
"Westwood Animal Hospital",
"Winter Garden Animal Hospital",
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

with open('jobs.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=jobs[0].keys())
    writer.writeheader()
    for job in jobs:
        writer.writerow(job)
    


