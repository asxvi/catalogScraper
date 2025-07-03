from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import requests
import string
import re
import os

# options = webdriver.ChromeOptions()
# # options.add_argument('--headless')  # add/ remove to see browser open
# options.add_argument('--disable-gpu')
# options.add_argument('--no-sandbox')

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# driver.get("https://webcs7.osss.uic.edu/schedule-of-classes/static/schedules/fall-2025/CS.html")
# time.sleep(1)  # let page load

# soup = BeautifulSoup(driver.page_source, 'html.parser')
# driver.quit()



# BASE_SPRING_URL = "https://webcs7.osss.uic.edu/schedule-of-classes/static/schedules/spring-2025/"
BASE_SPRING_URL = "https://webcs7.osss.uic.edu/schedule-of-classes/static/schedules/fall-2025/CS.html"


def getPrerequisites2(SUBJECT_URL):
    '''
        main function that might call helper to parse out all of the prerequisites for SUBJECT_URL in chosen semester

        PARAMETER: the link to specific subject.  i.e. 'https://webcs7.osss.uic.edu/schedule-of-classes/static/schedules/fall-2025/CS.html'
        RETURN: map of {str:Course -> str:Prereqs} .   i.e.  'CS141': 'CS111' ...
    '''
    rv_prereqs = {}
    response = requests.get(SUBJECT_URL)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        courses = soup.find_all('div', class_='col')
        
        # print(courses)

        translator = str.maketrans('', '', string.punctuation)              # https://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string

        for course in courses:
            course_name = course.find('h2') #.text.replace(' ', '___')
            print(course_name)
            course_description = course.find('p').text

            if 'Prerequisite(s):' in course_description:
                print(course_description)
                pre = course_description.split('Prerequisite(s):')[1]


                pattern = re.compile("\b([A-Z]{2,4})\s?(\d{2,3})\b")

                # pattern.findall()


                
                ##########################################################################################
                # # https://www.geeksforgeeks.org/python/python-remove-punctuation-from-string/#
                clean_text = pre.translate(translator)
                
                print(course_name,'\n' ,clean_text.split(), '\n')               # NOTE remove after debugging

                # # crazy how python literally has everythign built in lol 
                # # https://www.w3schools.com/python/ref_string_isnumeric.asp
                # prev = 0
                # for i, slice in enumerate(clean_text.split()):    
                #     if slice.isnumeric():
                #         print("___".join([clean_text.split()[i-1], slice]))
                #         if 'concurrent' in clean_text.split()[prev:i]:
                #             print('yoyo')

                #             '''
                #                 left off here last night. it works if i do this, but i gotta update the prev pointer each time that we find an actual value
                #             '''
                ##########################################################################################
    else:
        print(f'BAD response: {response.status_code}')


def getPrerequisites(SUBJECT_URL):
    '''
        main function that might call helper to parse out all of the prerequisites for SUBJECT_URL in chosen semester

        PARAMETER: the link to specific subject.  i.e. 'https://webcs7.osss.uic.edu/schedule-of-classes/static/schedules/fall-2025/CS.html'
        RETURN: map of {str:Course -> str:Prereqs} .   i.e.  'CS141': 'CS111' ...
    '''
    
    credit_hours_folderName = 'prereqDataStream/'
    semester_offerings_folderName = 'prereqDataStream/'
    
    response = requests.get(SUBJECT_URL)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        courses = soup.find_all('div', class_='courseblock')
        
        rv = ""
        for course in courses:            
            course_name = course.find('strong').text
            course_num = course_name.split()[0]
            course_name = (course_name.split()[0] + '___' + course_name.split()[1]).strip('.')
            course_description = course.find('p', class_='courseblockdesc').text
            
            prereqMatch = re.search("Prerequisite\s*(?:\(s\))?:\s*(.*)", course_description, re.IGNORECASE)
            if(prereqMatch):
                prereqs = prereqMatch.group(1)
                clean_prereqs = prereqs.replace("\xa0", '___')
                
                prevTaken = re.findall("Grade\s*of\s*[A-F]\s*or\s*better\s*in\s+([A-Z]{2,4}___[0-9]{2,3})", clean_prereqs, re.IGNORECASE)
                # concurrentTaken = re.findall("Credit\s*or\s*concurrent\s*registration\s*in\s+([A-Z]{2,4}___[0-9]{2,3})", clean_prereqs, re.IGNORECASE)
                concurrentTaken = re.findall("\s*concurrent\s*\s+([A-Z]{2,4}___[0-9]{2,3})", clean_prereqs, re.IGNORECASE)
                allNums = re.findall("([A-Z]{2,4}___[0-9]{2,3})", clean_prereqs, re.IGNORECASE)
                
                for c in allNums:
                    if c in prevTaken:
                        rv += (f'{c}\t{course_name}\t-1\n')
                    elif c in concurrentTaken:
                        print(f'{c}\t{course_name}\t0\n')
                        rv += (f'{c}\t{course_name}\t0\n')
                    else:
                        rv += (f'{c}\t{course_name}\t-1\n')
        
        if not os.path.isdir(f'data/{credit_hours_folderName}'):
            os.makedirs(f'data/{credit_hours_folderName}')
        if not os.path.isdir(f'data/{semester_offerings_folderName}'):      # can i move this outside the for loop
            os.makedirs(f'data/{semester_offerings_folderName}')

        with open(f"data/{credit_hours_folderName}prerequisites{course_num}.txt", 'w') as file:
            file.write(rv)
    else:
        print(f'BAD response: {response.status_code}')

if __name__ == "__main__":
    getPrerequisites('https://catalog.uic.edu/all-course-descriptions/chem/')