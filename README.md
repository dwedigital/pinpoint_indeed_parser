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

```bash
# Looks up a client name and will ask if you want to use fuzzy search and search as client or source name

python3 cli.py client

# after running the above you will be asked the client name. Once run you also have the option to exprt the jobs to a CSV that will save in the folder of the script

---

# Find a sepcific job and more detailed listing by job reference - good for debugging

python3 cli.py ref
```
