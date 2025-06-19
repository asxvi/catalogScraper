import selenium
from bs4 import BeautifulSoup
from scraper import scrapeFrontPage, scrapeSubject
from directoryFunctions import getAllSubjectCourses

''' contains URL links to various URL's used in program
'''
# [1]
BASE_URL = 'https://catalog.uic.edu/' #parent website used for building url
UIC_URL = 'https://catalog.uic.edu/all-course-descriptions/'



if __name__ == '__main__':
    print('running script')

    # these lines create all the files in data
    data = scrapeFrontPage()
    for d in data:
        scrapeSubject(data[d])
    
