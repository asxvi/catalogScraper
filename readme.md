# catalogScraper (need cooler name!)

## Project Structure
~catalogScraper
  ├── .gitignore: Specifies intentionally untracked files to ignore.
  ├── .venv/: Virtual environment for project dependencies (creates a directory with its own Python interpreter and package library, distinct from your system's global Python installatio).
  ├── requirements.txt: List of dependencies to install using pip.
  ├── scrapeNameCH.py: DONE Scrapes main catalog website, and writes to /data directory. (for now might need to make '/data' and '/dataCH' directory prior to running)
  ├── scrapeSemesters.py: DONE Scrapes specific website page for specific course and overwrites /dataCH and its files
  ├── scrapePrereq.py: CODING Scrapes prereq info, but needs to use Selenium and headless browser bc getting blocked by admin
  ├── main.py: IGNORE for now. Main script that will call other 3 .py files
  ├── headlessScrape.py IGNORE Scrapes prereq info, but needs to use Selenium and headless browser bc getting blocked by admin
  
  ## Setup
* Ensure Python 3.x is installed.
* Clone repo to local machine.
```
    git clone https://github.com/asxvi/catalogScraper.git
    cd catalogScraper
```
* Create and set up local virtual enviornment.
```
    python -m venv .venv
    source .venv/bin/activate   # Linux/ macOS
    pip install -r requirements.txt
```

## TODO
- [ ] complete prereq part
- [ ] merge into main.py and clean directory 
- [ ] add comments and improve readbility and usability by others
- [ ] Improve readme

## quick facts about UIC catalog:
about 7501 unique courses in UIC 2025 catalogue
FALL: NumSubjects: 168 NumCourses: 3157.
Spring: NumSubjects: 169 NumCourses: 3071.