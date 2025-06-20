from bs4 import BeautifulSoup
import requests
import re
from directoryFunctions import getAllSubjectCourses


# all semesters-  use this to update the 2 links below
# https://webcs7.osss.uic.edu/schedule-of-classes/static/index.php

# SPRING_URL = "https://webcs7.osss.uic.edu/schedule-of-classes/static/schedules/spring-2025/index.html"
# FALL_URL = "https://webcs7.osss.uic.edu/schedule-of-classes/static/schedules/fall-2025/index.html"
BASE_SPRING_URL = "https://webcs7.osss.uic.edu/schedule-of-classes/static/schedules/spring-2025/"
BASE_FALL_URL = "https://webcs7.osss.uic.edu/schedule-of-classes/static/schedules/fall-2025/"


def scrapeStaticFrontPage(BASE_URL):
    ''' 
        Called first to get all of the potenitally new subjects or subjects no longer offered. 
        NOTE MUST call for Spring and Fall individually. NOTE might make a helper function to call both spring and fall in 1 function call, but how do i return 2 rv's

        PARAMETER: the link to semester specific page.  i.e. BASE_SPRING_URL = 'https://webcs7.osss.uic.edu/schedule-of-classes/static/schedules/spring-2025/'
        RETURN key-value store in form: {Course Abbreviation: url to specific course info}
    '''
    response = requests.get(BASE_URL)
    major_links_dict = {}
    if response.status_code == 200:
        # continue with scraping        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 2 columns with all listed courses. find both and go thru each ones elements to get links
        # NOTE this portion is manual and subject to change with change in website design
        columns = soup.find_all('table', class_='table')
        for column in columns:
            subjects = column.find_all('tr')
            for subject in subjects:
                abbrev = subject.find('a').text
                linkExtension = subject.find('a')['href']
                major_links_dict[abbrev] = BASE_URL+linkExtension
    else:
        print(f'BAD response: {response.status_code}')
    return major_links_dict


# gets all of the courses for current subject. returns array [CS107, CS109...]
def getAllCourses(SUBJECT_URL):
    '''
        finds all of courses offered for SUBJECT_URL in the chosen semester

        PARAMETER: the link to specific subject.  i.e. 'https://webcs7.osss.uic.edu/schedule-of-classes/static/schedules/fall-2025/CS.html'
        RETURN: Array of course number strings.   i.e. 'CS101', 'CS141'...
    '''
    coursesInSemester = []
    response = requests.get(SUBJECT_URL)
    if response.status_code == 200:
        # continue with scraping
        soup = BeautifulSoup(response.content, 'html.parser')
        courses = soup.find_all('div', class_='row course')
        for course in courses:
            course_name = course.find('h2').text
            # course_name.replace(' ', '___')
            coursesInSemester.append(course_name.replace(' ', '___'))
    
    return coursesInSemester

# # all of the primary links to specific course info
# fallLinksDict = scrapeStaticFrontPage(BASE_FALL_URL)
# springLinksDict = scrapeStaticFrontPage(BASE_SPRING_URL)

# # fcs = (fallLinks['CS'])
# # scs = (fallLinks['CS'])

# # fall = getAllCourses(fallLinks)
# for link in fallLinksDict:
#     print(getAllCourses(fallLinksDict[link]))
#     break
# # spring = getAllCourses(scs)


FALLsemesterAvaliability = []
SPRINGsemesterAvaliability = []

# fallLinksDict = scrapeStaticFrontPage(BASE_FALL_URL)            # get all the links so we iter thru
# springLinksDict = scrapeStaticFrontPage(BASE_SPRING_URL)            # get all the links so we iter thru


fallLinksDict = ('https://webcs7.osss.uic.edu/schedule-of-classes/static/schedules/fall-2025/CS.html')

# for link in fallLinksDict:                                      # for every link we have to scrape indiv info
#     # abbrev = (getAllCourses(fallLinksDict[link])[0].split('_')[0])  # get part before number ex: CS    
#     avaliableCourses = getAllCourses(fallLinksDict[link])
#     for course in avaliableCourses:
#         FALLsemesterAvaliability.append(course)
#     break

avaliableCourses = getAllCourses(fallLinksDict)
for course in avaliableCourses:
    FALLsemesterAvaliability.append(course)
print(FALLsemesterAvaliability)


# for link in springLinksDict:                                      # for every link we have to scrape indiv info
#     avaliableCourses = getAllCourses(springLinksDict[link])
#     for course in avaliableCourses:
#         SPRINGsemesterAvaliability.append(course)

dir = './dataCH/'
getAllSubjectCourses(dir, FALLsemesterAvaliability)
