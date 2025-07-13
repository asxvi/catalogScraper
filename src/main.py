from scraping.scrapeNameCH import scrapeStage1, getLinks
from scraping.scrapeSemesters import scrapeStage2
from scraping.scrapePrereq import scrapeStage3
from dbFunctions import initDB

''' contains URL links to various URL's used in program'''
UIC_URL = 'https://catalog.uic.edu/all-course-descriptions/'                                           # used in stage 1 of scraping
BASE_FALL_URL = "https://webcs7.osss.uic.edu/schedule-of-classes/static/schedules/fall-2025/"          # used in stage 2 of scraping
BASE_SPRING_URL = "https://webcs7.osss.uic.edu/schedule-of-classes/static/schedules/spring-2025/"   



if __name__ == '__main__':
    print('Running script')

    links = getLinks(UIC_URL)
    
    scrapeStage1(links)
    scrapeStage2(BASE_FALL_URL, BASE_SPRING_URL)
    scrapeStage3(links)
    #scrapestage4 for timing
    
    initDB("uic_2425.db")

    print('Successful termination')
    
