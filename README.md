# Indeed Feed Parser

## Setup

Download or clone this git repo:
`git clone git@github.com:dwedigital/pinpoint_indeed_parser.git .`

Rename or copy `.env_example` to create a `.env` and update the `INDEED_FEED_URL`

Create the virtual env:
`python3 -m venv .venv`

Activate the virtual env:
`source .venv/bin/activate`

Install requirements:
`pip3 install -r requirements.txt`

## Usage

The main script is `cli.py` this is what you will run from the command line and search for a client or a job reference

There are 3 "options" when running the script:

1. `python3 cli.py client` - will allow you to search source name or client name
2. `python3 cli.py ref` - will ask you for the reference ID of a particular job. Useful for debugging a specific job as provides a lot more info on one job
3. `python3 cli.py` - with no options this will just return topline stats (number of jobs, sub-brands and companies in the feed)

Each time `cli.py` is run it will check the created time of the `indeed_feed_{date_time}.xml` file. If it does not exist or is older than 1 hour it will re-download and parse the feed and save a new XML file in your working directory. **This can take c. 2 mins longer**

### Client search

You will get asked if you want to use fuzzy search. 9 times out of 10 you likely will as this will look to see if your entered term/phrase is in the source name or client name as well as checking with or without spaces.

Sometimes if you are not finding a client you are 90% should be in there try doing more generic term i.e. `JSI` instead of `JSItel`.

If the results contain other companies then you likely do not want to use fuzzy search and then just search for the exact client/source name (case insensitve)

`source name` = the actual Pinpoint instance name (will typically be the main client name we know). This is useful is a clint had multiple themse which are seen as sub brands so we me have ACME (as a srouce name) with 3 jobs as `Company:ACME A` and 5 jobs as `Company:ACME B` but all will have `Source:ACME`

## `client_brands.py`

`client_brands.py` is a useful script if we are asked to look through a load of sub brands for one client and return all the jobs we can find for them.

1. You will need to update the array of brands with a list of comma seperated strings for each brand
2. Update the `client_name` varaible with a string containg the name of the client for use in file naming of the CSV export
