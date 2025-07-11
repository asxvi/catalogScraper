from scrapeNameCH import scrapeStage1, getLinks
from scrapeSemesters import scrapeStage2
from scrapePrereq import scrapeStage3

''' contains URL links to various URL's used in program'''
UIC_URL = 'https://catalog.uic.edu/all-course-descriptions/'                                           # used in stage 1 of scraping
BASE_FALL_URL = "https://webcs7.osss.uic.edu/schedule-of-classes/static/schedules/fall-2025/"          # used in stage 2 of scraping
BASE_SPRING_URL = "https://webcs7.osss.uic.edu/schedule-of-classes/static/schedules/spring-2025/"   



if __name__ == '__main__':
    print('Running script')

    links = getLinks(UIC_URL)
    

    # scrapeStage1(UIC_URL)
    # scrapeStage2(BASE_FALL_URL, BASE_SPRING_URL)

    # add scrapeStage3 which gets prereqs once thats done
    scrapeStage3(links)
    

    print('Successful termination')
    
