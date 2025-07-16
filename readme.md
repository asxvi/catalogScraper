# catalogScraper (need cooler name!)

## Project Structure 
```
~catalogScraper/
.
├── data/
│ 
├── debugging/
│   ├── debugging.md
│   ├── images/
├── readme.md
├── requirements.txt
├── src
│   ├── dbFunctions.py
│   ├── directoryFunctions.py
│   ├── main.py
│   └── scraping
│       ├── __init__.py
│       ├── scrapeNameCH.py
│       ├── scrapePrereq.py
│       ├── scrapeSemesters.py
│       └── scrapeTiming.py
└── uic_2425.db
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

## Usage:
* Complete Setup step above.
* run main.py using python 3.x
```
    python3 src/main.py
```
* Access embedded duckDB database
```
  duckdb [name of db] -ui
  # https://duckdb.org/docs/stable/index
```


## Quick facts about UIC catalog:
* about 7501 unique courses in UIC 2025 catalogue
* FALL: NumSubjects: 168 NumCourses: 3157.
* Spring: NumSubjects: 169 NumCourses: 3071.

## TODO
- [ ] Improve readme and documentation
- [ ] add timestamps to DB of ingestion date/ updated date.
- [ ] Implement UIS, UIUC scraping and logic, and DB.
- [X] complete prereq part.
- [X] merge into main.py and clean directory.
- [X] add comments and improve readbility and usability by others.
- [X] modify semesters no default value of 0 0.