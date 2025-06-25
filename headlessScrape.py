from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import requests
from bs4 import BeautifulSoup
import string
import re

options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # add/ remove to see browser open
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://webcs7.osss.uic.edu/schedule-of-classes/static/schedules/fall-2025/CS.html")
time.sleep(2)  # let page load

soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()



BASE_SPRING_URL = "https://webcs7.osss.uic.edu/schedule-of-classes/static/schedules/spring-2025/"


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
        print(soup)
        courses = soup.find_all('div', class_='col')
        print(courses)
        translator = str.maketrans('', '', string.punctuation)              # https://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string

        for course in courses:
            course_name = course.find('h2').text.replace(' ', '___')
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



if __name__ == "__main__":
    getPrerequisites(BASE_SPRING_URL)