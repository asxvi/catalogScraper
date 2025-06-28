# catalogScraper (need cooler name!)

## Project Structure 
```
~catalogScraper
├── .gitignore: Specifies intentionally untracked files to ignore.tre
├── .venv/: Virtual environment for project dependencies (creates a directory with its own Python interpreter and package library, distinct from your system's global Python installatio).
├── data/: stores data about every course and number of credits it can be 
├── dataCH/: stores data about the semester a course is avaliable in
├── directoryFunctions.py: file to clearing the data/ and dataCH/ directories as well as other dir utilities
├── examples/: personal files for reference 
├── headlessScrape.py: IGNORE
├── main.py: IGNORE
├── requirements.txt: List of dependencies to install using pip.
├── scrapePrereq.py Working on this
├── scrapeSemesters.py: DONE Scrapes specific website page for specific course and overwrites /dataCH and its files
├── scrapeNameCH.py: DONE Scrapes main catalog website, and writes to /data directory. (for now might need to make '/data' and '/dataCH' directory prior to running)
```


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

- [ ] complete prereq
- [ ] modify semesters no default value of 0 0 
- [ ] add time 

## quick facts about UIC catalog:
about 7501 unique courses in UIC 2025 catalogue
FALL: NumSubjects: 168 NumCourses: 3157.
Spring: NumSubjects: 169 NumCourses: 3071.
