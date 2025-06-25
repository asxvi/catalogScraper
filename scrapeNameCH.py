from bs4 import BeautifulSoup
import requests
import re


BASE_URL = 'https://catalog.uic.edu/' #parent website used for building url
UIC_URL = 'https://catalog.uic.edu/all-course-descriptions/'


def convHoursStrToRange(hours_str):
    '''
        Hours come out strange compared to the desired output, so we have to manually parse them
        based on the 3 possibilities for credit hours: 'n' credits, 'n-m' credits, 'n or m' credits    
        
        PARAM: the string to parse/ reformat into a range 
        RETURN: tuple of range: (smaller_num_possible_credits, larger_num_possible_credits)
    '''

    # remove the words hour or hours and remove all extra white space
    clean_str = hours_str.lower().replace("hours", "").replace("hour", "").strip()
    first_num = None; second_num = None
    
    # first check for range, and take values to left and right of '-'
    if '-' in clean_str:
        first_num, second_num = clean_str.split('-')
    # otherwise the credits are either 'n or m' credits or 'n' credits
    elif 'or' in clean_str:
        items = clean_str.split('or')
        first_num = items[0].strip()
        second_num = items[1].strip()
    else:
        first_num = clean_str
        second_num = clean_str

    return (first_num, second_num)


def convHourRangeToList(hours_str):
    '''
        Call convHoursStrToRange helper function and return a string of the entire 
        range of credit hours for the course. 
        
        PARAM: the string to parse/ reformat into a range using convHoursStrToRange
        RETURN: a string of all possible credit hours. Ex: "3,4,5...", or just '3' ...
        Note: Have to convert from int to str a few times within this entire process
    '''

    first_num, second_num = convHoursStrToRange(hours_str)
    rv = []
    
    # the range (first_num, second_num) should be 2 int values cast as strings. if not then we get ERROR
    try:
        first_num = int(first_num)
        second_num = int(second_num)
    except ValueError:
        print(f"Can't parse the hours {hours_str}. Should be able to cast str as an int. Ex: int('5') == 5")
        rv = []

    # either the CH range is 1 value ex: (3, 3) == '3', or multiple values ex: (1, 4) == '1,2,3,4'
    if first_num == second_num:
        rv = [first_num]
    else:
        rv = list(range(first_num, second_num + 1))

    return(','.join(map(str, rv)))


def scrapeFrontPage(URL):
    '''

    '''
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
        ^([A-Z]+)\s+(\d+)\.              #subject and course number ex: 'CS 100.'
        \s+(.+?[.?!])                       # course title, non-greedy up to next period
        # \s+(\d+(?:\s*-\s*\d+|\s+or\s+\d+)?\s*hour)\.?$  # Hour: 3, 1-3, or '3 or 4'                         
        \s+(\d+(?:\s*-\s*\d+|\s+or\s+\d+)?\s*hours?)\.?$  # Hours: 3, 1-3, or '3 or 4'
    """, re.VERBOSE)

    for course in allCourses:
        course_title_hours = (course.find('p', class_='courseblocktitle').text)
        match = pattern.match(course_title_hours)
        
        if match:
            subject = match.group(1)
            number = match.group(2)
            course_title = match.group(3).strip()
            course_hours = match.group(4).strip()
            
            course_num = f"{subject}___{number}"  # delimit with whatever, this follows example 6/16/25
            
            # debugging
            # print(f"Code: {course_num}, Title: {course_title}, Hours: {course_hours}")
            course_hours = (convHourRangeToList(course_hours))
            
            subject = "".join(char for char in course_num if char.isalpha())
            # write to 2 different files. this should reduce the runtime by a little
            # note it seemslike this works 57 runtime for 2 writes
            with open(f"data/mastercourselist_{subject}.txt", 'a') as file:
                file.write(f"{course_num}\t{course_hours}\n")
            with open(f"dataCH/courseofferings_{subject}.txt", 'a') as file:
                file.write(f"{course_num}\t0\t0\n")
        else:
            print(course_title_hours)
            print(match)

# scrape webpage and return a txt file 
# this function needs to be called for each subject. must be inside for loop with 
# input being the url for the current subject. returns array of just course names
def getCourseNames(URL_subject):
    response = requests.get(URL_subject)

    if response.status_code == 200:
        # continue with scraping
        soup = BeautifulSoup(response.content, 'html.parser')
        courseBlock = soup.find('div', class_="sc_sccoursedescs")
        allCourses = courseBlock.find_all('div', class_='courseblock')

        rv = []

        pattern = re.compile(r"""
            ^([A-Z]+)\s+(\d+)\.              #subject and course number ex: 'CS 100.'
            \s+(.+?[.?!])                       # course title, non-greedy up to next period
            # \s+(\d+(?:\s*-\s*\d+|\s+or\s+\d+)?\s*hour)\.?$  # Hour: 3, 1-3, or '3 or 4'                         
            \s+(\d+(?:\s*-\s*\d+|\s+or\s+\d+)?\s*hours?)\.?$  # Hours: 3, 1-3, or '3 or 4'
        """, re.VERBOSE)

        for course in allCourses:
            course_title_hours = (course.find('p', class_='courseblocktitle').text)
            match = pattern.match(course_title_hours)
            
            if match:
                subject = match.group(1)
                number = match.group(2)            
                course_num = f"{subject} {number}"  # delimit with whatever, this follows example 6/16/25
                
                rv.append(course_num)
                
            else:
                print(course_title_hours)
                print(match)
        return rv

    else:
        print(f'BAD response: {response.status_code}')


data = scrapeFrontPage(UIC_URL)

# csLink = data['Computer Science (CS)']   #testing data point
# scrapeSubject(csLink)

for d in data:
    scrapeSubject(data[d])
