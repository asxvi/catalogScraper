from bs4 import BeautifulSoup
import requests
import re
from scraper import getCourseNames, scrapeFrontPage


# all semesters-  use this to update the 2 links below
# https://webcs7.osss.uic.edu/schedule-of-classes/static/index.php
# SPRING_URL = "https://webcs7.osss.uic.edu/schedule-of-classes/static/schedules/spring-2025/index.html"
# FALL_URL = "https://webcs7.osss.uic.edu/schedule-of-classes/static/schedules/fall-2025/index.html"

BASE_SPRING_URL = "https://webcs7.osss.uic.edu/schedule-of-classes/static/schedules/spring-2025/"
BASE_FALL_URL = "https://webcs7.osss.uic.edu/schedule-of-classes/static/schedules/fall-2025/"


def scrapeStaticFrontPage(BASE_URL):
    response = requests.get(BASE_URL)
    major_links_dict = {}
    if response.status_code == 200:
        # continue with scraping
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 2 columns with all listed courses. find both and go thru each ones elements to get links
        # this portion is manual and subject to change with change in website design
        subjects = soup.find_all('table', class_='table')
        for subject in subjects:
            allSubjects = subject.find_all('tr')
            for elem in allSubjects:
                abbrev = elem.find('a').text
                linkExtension = elem.find('a')['href']
                major_links_dict[abbrev] = BASE_URL+linkExtension
    else:
        print(f'BAD response: {response.status_code}')
    return major_links_dict


# gets all of the coruses for current subject. returns array [CS107, CS109...]
def getAllCourses(SUBJECT_URL):
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

fallLinks = scrapeStaticFrontPage(BASE_FALL_URL)
springLinks = scrapeStaticFrontPage(BASE_SPRING_URL)

fcs = (fallLinks['CS'])
scs = (fallLinks['CS'])

spring = getAllCourses(fcs)
spring = getAllCourses(scs)
