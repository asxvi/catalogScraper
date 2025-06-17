from bs4 import BeautifulSoup
import requests
import re


BASE_URL = 'https://catalog.uic.edu/' #parent website used for building url
UIC_URL = 'https://catalog.uic.edu/all-course-descriptions/'

def parseHours(hours_str):
    hour_str = hour_str.split().lower().replace('hours', '').strip()
    print(hour_str)

def scrapeFrontPage():
    major_links_dict = {}
    
    response = requests.get(UIC_URL)
    if response.status_code == 200:
        # continue with scraping
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # target the sitemap in main body and not the left menu
        siteMap = soup.find('div', class_='sitemap')
        allMajors = siteMap.find_all('a', class_='sitemaplink')

        # debugging, store as list and kv store
        major_links_list = []
        
        for major in allMajors:
            major_links_list.append(BASE_URL + major['href'])
            major_links_dict[major.text] = (BASE_URL + major['href'])

    else:
        print(f'BAD response: {response.status_code}')

    return major_links_dict


def scrapeSubject(URL_subject):
    response = requests.get(URL_subject)

    if response.status_code == 200:
        # continue with scraping
        soup = BeautifulSoup(response.content, 'html.parser')
        courseBlock = soup.find('div', class_="sc_sccoursedescs")
        allCourses = courseBlock.find_all('div', class_='courseblock')

        getMasterCourseList(allCourses)

    else:
        print(f'BAD response: {response.status_code}')
    
# scrape webpage and return a txt file 
def getMasterCourseList(allCourses):
    baseFilename = 'mastercourselist'

    pattern = re.compile(r"""
        ^([A-Z]+)\s?(\d+)\.              #subject and course number ex: 'CS 100.'
        \s+(.+?)\.                       # course title, non-greedy up to next period
        # \s+(\d+(?:\s*-\s*\d+|\s+or\s+\d+)?\s*hour)\.?$  # Hour: 3, 1-3, or '3 or 4'                         
        \s+(\d+(?:\s*-\s*\d+|\s+or\s+\d+)?\s*hours?)\.?$  # Hours: 3, 1-3, or '3 or 4'
    """, re.VERBOSE)

    for course in allCourses:
        course_title_hours = (course.find('p', class_='courseblocktitle').text)
        # print(course_title_hours)
        
        match = pattern.match(course_title_hours)
        
        if match:
            subject = match.group(1)
            number = match.group(2)
            course_title = match.group(3).strip()
            course_hours = match.group(4).strip()
            
            course_num = f"{subject}___{number}"  # delimit with whatever
            
            # debugging
            # print(f"Code: {course_num}, Title: {course_title}, Hours: {course_hours}")
 
            # parseHours(course_hours)
            
            subject = "".join(char for char in course_num if char.isalpha())
            with open(f"data/mastercourselist_{subject}.txt", 'a') as file:
                file.write(f"{course_num}\t{course_hours}\n")
        else:
            print(course_title_hours)

# def writeToFile(filename:str):
#   pass

data = scrapeFrontPage()
# csLink = data['Computer Science (CS)']
# scrapeSubject(csLink)

for d in data:
    scrapeSubject(data[d])

