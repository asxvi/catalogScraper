from bs4 import BeautifulSoup
import requests
import re
import string
from directoryFunctions import getAllSubjectCourses

import time

start = time.time()

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


def getPrerequisites(SUBJECT_URL):
    '''
        main function that might call helper to parse out all of the prerequisites for SUBJECT_URL in chosen semester

        PARAMETER: the link to specific subject.  i.e. 'https://webcs7.osss.uic.edu/schedule-of-classes/static/schedules/fall-2025/CS.html'
        RETURN: map of {str:Course -> str:Prereqs} .   i.e.  'CS141': 'CS111' ...
    '''
    rv_prereqs = {}
    response = requests.get(SUBJECT_URL)
    if response.status_code == 200:
        # continue with scraping
        soup = BeautifulSoup(response.content, 'html.parser')
        courses = soup.find_all('div', class_='row course')
        translator = str.maketrans('', '', string.punctuation)              # https://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string

        for course in courses:
            course_name = course.find('h2').text.replace(' ', '___')
            course_description = course.find('p').text

            if 'Prerequisite(s):' in course_description:
                pre = course_description.split('Prerequisite(s):')[1]

                # https://www.geeksforgeeks.org/python/python-remove-punctuation-from-string/#
                clean_text = pre.translate(translator)
                
                print(course_name,'\n' ,clean_text.split(), '\n')               # NOTE remove after debugging

                # crazy how python literally has everythign built in lol 
                # https://www.w3schools.com/python/ref_string_isnumeric.asp
                prev = 0
                for i, slice in enumerate(clean_text.split()):    
                    if slice.isnumeric():
                        print("___".join([clean_text.split()[i-1], slice]))
                        if 'concurrent' in clean_text.split()[prev:i]:
                            print('yoyo')


# '''######'''
# FALLsemesterAvaliability = []
# SPRINGsemesterAvaliability = []

# fallLinksDict = scrapeStaticFrontPage(BASE_FALL_URL)            # get all the links so we iter thru
# springLinksDict = scrapeStaticFrontPage(BASE_SPRING_URL)            # get all the links so we iter thru
# # fallLinksDict = ('https://webcs7.osss.uic.edu/schedule-of-classes/static/schedules/fall-2025/CS.html')
# # springLinksDict = ('https://webcs7.osss.uic.edu/schedule-of-classes/static/schedules/spring-2025/CS.html')

# for link in fallLinksDict:                                      # for every link we have to scrape indiv info
#     avaliableCourses = getAllCourses(fallLinksDict[link])
#     for course in avaliableCourses:
#         FALLsemesterAvaliability.append(course)
# dir = './dataCH/'
# getAllSubjectCourses(dir, FALLsemesterAvaliability, 'fall')

# fall = time.time()
# print(f'fall: {fall-start}')


# for link in springLinksDict:                                      # for every link we have to scrape indiv info
#     avaliableCourses = getAllCourses(springLinksDict[link])
#     for course in avaliableCourses:
#         SPRINGsemesterAvaliability.append(course)
# dir = './dataCH/'
# getAllSubjectCourses(dir, SPRINGsemesterAvaliability, 'spring')

# spring = time.time()
# print(f'spring: {spring-start}')
# '''######'''


# end = time.time()
# print(end-start)



if __name__ == "__main__":
    fallLinksDict = ('https://webcs7.osss.uic.edu/schedule-of-classes/static/schedules/fall-2025/CS.html')
    getPrerequisites(fallLinksDict)