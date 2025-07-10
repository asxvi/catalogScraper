from bs4 import BeautifulSoup
import requests
import string
from typing import List
import os

# https://webcs7.osss.uic.edu/schedule-of-classes/static/index.php          # contains archive of all (recent) semesters
# BASE_SPRING_URL = "https://webcs7.osss.uic.edu/schedule-of-classes/static/schedules/spring-2025/"
# BASE_FALL_URL = "https://webcs7.osss.uic.edu/schedule-of-classes/static/schedules/fall-2025/"


def scrapeStage2(BASE_FALL_URL: str, BASE_SPRING_URL: str) -> None:
    '''
        Uses helper functions: scrapeStaticFrontPage(), getAllCoursesSemester(), writeSubjectCourses(), and removeUnavaliableCourses() to
            - Update all offerings files based on actual semesters a course is avaliable in
            - Remove any courses that are not avalaible in either semester ex: CS100 0 0

        Parameters:
            BASE_FALL_URL (str): Page to scrape all courses avaliable in fall
            BASE_SPRING_URL (str): Page to scrape all courses avaliable in spring
        Returns:
            None: On successful exit. Print to console
    '''
    
    FALLsemesterAvaliability, SPRINGsemesterAvaliability = [], []
    fallLinksDict = scrapeStaticFrontPage(BASE_FALL_URL)                # get all the links so we iter thru
    springLinksDict = scrapeStaticFrontPage(BASE_SPRING_URL)            # get all the links so we iter thru

    for link in fallLinksDict:                                      # for every link we have to scrape indiv info
        avaliableCourses = getAllCoursesSemester(fallLinksDict[link])
        for course in avaliableCourses:
            FALLsemesterAvaliability.append(course)

    for link in springLinksDict:                                      # for every link we have to scrape indiv info
        avaliableCourses = getAllCoursesSemester(springLinksDict[link])
        for course in avaliableCourses:
            SPRINGsemesterAvaliability.append(course)
    
    dir = "./data/offeringsDataBatch/"                # do not change. Might add feature to change
    writeSubjectCourses(dir, FALLsemesterAvaliability, 'fall')
    writeSubjectCourses(dir, SPRINGsemesterAvaliability, 'spring')

    removeUnavaliableCourses(dir)

    print("Successfully wrote and modified to offeringsData")


def scrapeStaticFrontPage(URL: str) -> dict:
    ''' 
        Get all the subjects and direct links to later iterate through each individual subjects semester and prereqs
        
        Parameters:
            URL (str): the link to semester specific page.  i.e. BASE_SPRING_URL or BASE_FALL_URL
        Returns:
            major_links_dict (dict {str: str}): key-value store in form: {Course Abbreviation: url to specific course info}
        Debugging: 
            visit /dubugging
            Errors may stem from lines that contain '.find()' or '.find_all'
    '''
    major_links_dict = {}

    response = requests.get(URL)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 2 columns with all listed courses. find both and go thru each ones elements to get links
        columns = soup.find_all('table', class_='table')
        for column in columns:
            subjects = column.find_all('tr')
            for subject in subjects:
                abbrev = subject.find('a').text
                linkExtension = subject.find('a')['href']

                major_links_dict[abbrev] = URL+linkExtension
    else:
        print(f'BAD response: {response.status_code}')

    return major_links_dict


def getAllCoursesSemester(SUBJECT_URL: str) -> list:
    '''
        Finds all of courses offered for SUBJECT_URL in the chosen semester
        
        Parameters: 
            SUBJECT_URL (str): the link to specific subject.  i.e. 'https://webcs7.osss.uic.edu/schedule-of-classes/static/schedules/fall-2025/CS.html'
        Returns: 
           coursesInSemester (list): array of course number strings.   i.e. 'CS101', 'CS141'...
        Debugging: 
            visit /dubugging
            Errors may stem from lines that contain '.find()' or '.find_all'
    '''
    coursesInSemester = []
    response = requests.get(SUBJECT_URL)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        courses = soup.find_all('div', class_='row course')
        for course in courses:
            course_name = course.find('h2').text
            coursesInSemester.append(course_name.replace(' ', '___'))
    else:
        print(f'BAD response: {response.status_code}')
    return coursesInSemester


def writeSubjectCourses(directory: str, avaliableCourses: list, semester: str) -> None:
    '''
        Iterate through every course in avaliableCourses, and change bool from 0 to 1
        in offerings .txt file if course is avaliable in current semester.

        Parameters:
            directory (str): name of directory that we store offerings data
            avaliableCourses (list): every course avaliable for subject in current semester
            semester (str): either fall(FW) or spring(SS)
        Returns:
            None:
    '''
    if semester.lower() == 'fall' or semester.lower() == 'spring':
        for file in sorted(os.listdir(directory)):                      # sort directory alphabetically like it shows in actual dir
                if file == '.*' or file == '.DS_Store':
                    continue
                
                fullPath = f'{directory}{file}'

                # if fullPath == './data/offeringsDataBatch/courseofferings_CS.txt':

                # read file in, and compare if every course is in avaliableCourses for current semester
                with open(fullPath, 'r', encoding='utf-8') as openedFile:
                    lines = openedFile.readlines()

                updatedLines = []           # stores all non updated and updated strings in format: 'CS___101\t1\t0'
                for i, line in enumerate(lines):
                    parts = line.strip().split()
                    
                    if parts and parts[0] in avaliableCourses and semester.lower() == 'fall':
                        parts[1] = '1'
                    elif parts and parts[0] in avaliableCourses and semester.lower() == 'spring':
                        parts[2] = '1' 
                    updatedLines.append('\t'.join(parts) + '\n')
        
                # cant easily update file in place, so have to write over existing information... ig thats the best way shrug
                with open(fullPath, 'w') as openedFile:
                    openedFile.writelines(updatedLines)
    else:
        print("semester parameter should be either 'fall' or 'spring'.")


def removeUnavaliableCourses(directory: str) -> None:
    '''
        One last function to go thorough every file and finally remove all courses not offered
        in either spring or fall semester. ex: "CS100    0   0" would get removed.

        Parameters:
            directory (str): directory of where we are saving file output
        Returns:
            None:
    '''
    for file in sorted(os.listdir(directory)):                      # sort directory alphabetically like it shows in actual dir
                if file == '.*' or file == '.DS_Store':
                    continue

                fullPath = f'{directory}{file}'
                
                # if fullPath == './data/offeringsDataBatch/courseofferings_CS.txt':

                # read file in, and compare if every course is in avaliableCourses for current semester
                with open(fullPath, 'r', encoding='utf-8') as openedFile:
                    lines = openedFile.readlines()

                updatedLines = []           # stores all non updated and updated strings in format: 'CS___101\t1\t0'
                for i, line in enumerate(lines):
                    parts = line.strip().split()
                    # print(parts)
                    
                    if parts and parts[1] == '0' and parts[2] == '0':
                        continue
                    else:
                        updatedLines.append('\t'.join(parts) + '\n')
        
                # # cant easily update file in place, so have to write over existing information... ig thats the best way shrug
                with open(fullPath, 'w') as openedFile:
                    openedFile.writelines(updatedLines)


# def getPrerequisites(SUBJECT_URL):
#     '''
#         main function that might call helper to parse out all of the prerequisites for SUBJECT_URL in chosen semester

#         PARAMETER: the link to specific subject.  i.e. 'https://webcs7.osss.uic.edu/schedule-of-classes/static/schedules/fall-2025/CS.html'
#         RETURN: map of {str:Course -> str:Prereqs} .   i.e.  'CS141': 'CS111' ...
#     '''
#     rv_prereqs = {}
#     response = requests.get(SUBJECT_URL)
#     if response.status_code == 200:
#         # continue with scraping
#         soup = BeautifulSoup(response.content, 'html.parser')
#         courses = soup.find_all('div', class_='row course')
#         translator = str.maketrans('', '', string.punctuation)              # https://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string

#         for course in courses:
#             course_name = course.find('h2').text.replace(' ', '___')
#             course_description = course.find('p').text

#             if 'Prerequisite(s):' in course_description:
#                 print(course_description)
#                 # pre = course_description.split('Prerequisite(s):')[1]


#                 # pattern = re.compile("\b([A-Z]{2,4})\s?(\d{2,3})\b")

#                 # pattern.findall()

                
#                 ##########################################################################################
#                 # # https://www.geeksforgeeks.org/python/python-remove-punctuation-from-string/#
#                 # clean_text = pre.translate(translator)
                
#                 # print(course_name,'\n' ,clean_text.split(), '\n')               # NOTE remove after debugging

#                 # # crazy how python literally has everythign built in lol 
#                 # # https://www.w3schools.com/python/ref_string_isnumeric.asp
#                 # prev = 0
#                 # for i, slice in enumerate(clean_text.split()):    
#                 #     if slice.isnumeric():
#                 #         print("___".join([clean_text.split()[i-1], slice]))
#                 #         if 'concurrent' in clean_text.split()[prev:i]:
#                 #             print('yoyo')

#                 #             '''
#                 #                 left off here last night. it works if i do this, but i gotta update the prev pointer each time that we find an actual value
#                 #             '''
#                 ##########################################################################################
#     else:
#         print(f'BAD response: {response.status_code}')

# if __name__ == "__main__":
#     getPrerequisites('https://webcs7.osss.uic.edu/schedule-of-classes/static/schedules/spring-2025/CS.html')


"""'''######'''
FALLsemesterAvaliability = []
SPRINGsemesterAvaliability = []

fallLinksDict = scrapeStaticFrontPage(BASE_FALL_URL)            # get all the links so we iter thru
springLinksDict = scrapeStaticFrontPage(BASE_SPRING_URL)            # get all the links so we iter thru
# fallLinksDict = ('https://webcs7.osss.uic.edu/schedule-of-classes/static/schedules/fall-2025/CS.html')
# springLinksDict = ('https://webcs7.osss.uic.edu/schedule-of-classes/static/schedules/spring-2025/CS.html')

for link in fallLinksDict:                                      # for every link we have to scrape indiv info
    avaliableCourses = getAllCoursesSemester(fallLinksDict[link])
    for course in avaliableCourses:
        FALLsemesterAvaliability.append(course)

for link in springLinksDict:                                      # for every link we have to scrape indiv info
    avaliableCourses = getAllCoursesSemester(springLinksDict[link])
    for course in avaliableCourses:
        SPRINGsemesterAvaliability.append(course)

dir = './data/offeringsDataBatch/'
writeSubjectCourses(dir, FALLsemesterAvaliability, 'fall')
writeSubjectCourses(dir, SPRINGsemesterAvaliability, 'spring')


# FOR testing with only CS value
# avaliableCourses = getAllCoursesSemester(fallLinksDict)
# writeSubjectCourses(dir, avaliableCourses, 'fall')
# print()
# avaliableCourses = getAllCoursesSemester(springLinksDict)
# writeSubjectCourses(dir, avaliableCourses, 'spring')
# removeUnavaliableCourses(dir)"""