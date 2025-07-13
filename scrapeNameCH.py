from bs4 import BeautifulSoup
import requests
import re
from typing import List
import os

def getLinks(UIC_URL: str) -> dict:
    return scrapeCatalogFrontPage(UIC_URL)

# def scrapeStage1(UIC_URL: str) -> dict:
def scrapeStage1(links):
    '''
        Uses helper functions: scrapeCatalogFrontPage(), and writeCourseInfoToFileBatch() to 
        - Write to CH file all subjects the number of credit hours they take
        - Write to semester offerings file default values: COURSE 0 0 (for later use)

        Parameters:
            UIC_URL (str): UIC catalog homepage. Only used in part 1
        Returns:
            data (dict {str: str}): On successful exit. Print to console and return dict of direct links 
    '''

    # data = scrapeCatalogFrontPage(UIC_URL
    # for subject in data:
    for subject in links:
        writeCourseInfoToFileBatch(links[subject])                       # use Batch and not Stream function

    print("Successfully wrote to dataCreditHours and dataSemesters")


def convHoursStrToRange(hours_str: str) -> tuple:
    '''
        Hours come out strange compared to the desired output, so we have to manually parse them
        based on the 3 possibilities for credit hours: 'n' credits, 'n-m' credits, 'n or m' credits    
        
        Parameters: 
            hours_str (str): the string to parse/reformat into a range 
        Returns: 
            (first_num, second_num) (tuple): A range of possible credits(smaller_num_possible_credits, larger_num_possible_credits)
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


def convHourRangeToList(hours_str: str) -> str:
    '''
        Call convHoursStrToRange helper function and return a string of the entire 
        range of credit hours for the course. 

        Parameters: 
            hours_str (str): the string to parse/ reformat into a range using convHoursStrToRange 
        Returns: 
            (str): a string of all possible credit hours. Ex: "3,4,5...", or just '3'...
        Note: 
            Have to convert from int to str a few times within this entire process
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

    # map applies a function: str() to every value in rv
    return(','.join(map(str, rv)))


def scrapeCatalogFrontPage(URL: str) -> dict:
    '''
        Scrape https://catalog.uic.edu/all-course-descriptions/ for every subject 
        and link to specific subject page
        
        Parameters:
            URL (str): string to UIC catalog URL. https://catalog.uic.edu/all-course-descriptions/
        Returns:
            major_links_dict (str: str): key is Subject and value is link to more subject info 
            ex: (CS: https://webcs7.osss.uic.edu/schedule-of-classes/static/schedules/fall-2025/CS.html)
        Debugging: 
            visit /dubugging
            Errors may stem from lines that contain '.find()' or '.find_all'
            Erros may stem from Base_URL changing
    '''

    BASE_URL = 'https://catalog.uic.edu/'               # may break if URL changes
    major_links_dict = {}
    
    response = requests.get(URL)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # target the sitemap in main body and not the left menu. May change with time
        siteMap = soup.find('div', class_='sitemap')
        allMajors = siteMap.find_all('a', class_='sitemaplink')
    
        for major in allMajors:
            major_links_dict[major.text] = (BASE_URL + major['href'])
    else:
        print(f'BAD response: {response.status_code}')

    return major_links_dict


def writeCourseInfoToFileStream(URL_subject: str) -> None:
    '''
        Scrape specific subject and call helper function to create files inside /{path_to_folder_with_credit_hours}. 

        Parameters:
            URL_subject (str): string to specific UIC subject URL. ex: https://webcs7.osss.uic.edu/schedule-of-classes/static/schedules/fall-2025/CS.html
        Returns:
            None:
            helper function creates files inside /{path_to_folder_with_credit_hours}. 
        Debugging: 
            visit /dubugging
            Errors may stem from lines that contain '.find()' or '.find_all'
    '''
    response = requests.get(URL_subject)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        courseBlock = soup.find('div', class_="sc_sccoursedescs")
        allCourses = courseBlock.find_all('div', class_='courseblock')

        # helper function to go thru every course in curr subject
        coursePatternMatchStream(allCourses)              

    else:
        print(f'BAD response: {response.status_code}')
    

def coursePatternMatchStream(allCourses: str) -> None:
    '''
        Parameters:
            allCourses (str): a DOM-like that contains HTML map that we parse
        Returns:
            None:
            Create files in directory, but no rv
        Debugging: 
            visit /dubugging
            Errors may stem from lines that contain '.find()' or '.find_all'
    '''

    credit_hours_folderName = 'CHdataStream/'
    semester_offerings_folderName = 'offeringsDataStream/'

    pattern = re.compile(r"""
        ^([A-Z]+)\s+(\d+)\.                                     # subject and course number ex: 'CS 100.'
        \s+(.+?[.?!])                                           # course title, non-greedy up to next period
        \s+(\d+(?:\s*-\s*\d+|\s+or\s+\d+)?\s*hours?)\.?$        # hour(s): 3, 1-3, or '3 or 4'
    """, re.VERBOSE)

    for course in allCourses:
        course_title_hours = (course.find('p', class_='courseblocktitle').text)
        match = pattern.match(course_title_hours)
        
        if match:
            course_subject = match.group(1)
            course_number = match.group(2)
            course_title = match.group(3).strip()
            course_hours = match.group(4).strip()
            
            course_num = f"{course_subject}___{course_number}"  # delimit with whatever, this follows example 6/16/25
            course_hours = (convHourRangeToList(course_hours))
            course_subject = "".join(char for char in course_num if char.isalpha())
            
            # print(f"Code: {course_num}, Title: {course_title}, Hours: {course_hours}")            # debugging

            if not os.path.isdir(f'data/{credit_hours_folderName}'):
                os.makedirs(f'data/{credit_hours_folderName}')
            if not os.path.isdir(f'data/{semester_offerings_folderName}'):
                os.makedirs(f'data/{semester_offerings_folderName}')
            
            # write to 2 different files. this should reduce the runtime by a little

            with open(f"data/{credit_hours_folderName}mastercourselist_{course_subject}.txt", 'a') as file:
                file.write(f"{course_num}\t{course_hours}\n")
            with open(f"data/{semester_offerings_folderName}courseofferings_{course_subject}.txt", 'a') as file:
                file.write(f"{course_num}\t0\t0\n")
        else:
            print(f"Error writiting to {course_subject}")
            print(course_title_hours)


def writeCourseInfoToFileBatch(URL_subject: str) -> None:
    '''
        calls pattern match helper function for every course. write to file all subjects and credit hours
        
        Parameters:
            URL_subject (str): Current subject to scrape all courses for
        Returns:
            None: 
            write to file for current subject
        Debugging: 
            visit /dubugging
            Errors may stem from lines that contain '.find()' or '.find_all'
    '''

    credit_hours_folderName = 'dataCreditHours/'
    semester_offerings_folderName = 'dataSemesters/'

    response = requests.get(URL_subject)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        courseBlock = soup.find('div', class_="sc_sccoursedescs")
        allCourses = courseBlock.find_all('div', class_='courseblock')

        # helper function to go thru every course in curr subject
        writeOnce = ["", ""]        # stores strings to batch insert into 2 files
        for course in allCourses:
            course_title_hours = (course.find('p', class_='courseblocktitle').text)
            course_subject = coursePatternMatchBatch(course_title_hours, writeOnce)

            if not os.path.isdir(f'data/{credit_hours_folderName}'):
                os.makedirs(f'data/{credit_hours_folderName}')
            if not os.path.isdir(f'data/{semester_offerings_folderName}'):      # can i move this outside the for loop
                os.makedirs(f'data/{semester_offerings_folderName}')

        # Special case of adding the final course for each subject
        writeOnce[0] += (f"{course_subject}___XXX\t{0}\n")
        writeOnce[1] += (f"{course_subject}___XXX\t0\t0\n")

        # batch write to 2 files. 1 write per each file, for each subject. 
        # Should be 2 * numSubject writes in this step alone vs 3000+ indiv writes if write for each course
        with open(f"data/{credit_hours_folderName}mastercourselist_{course_subject}.txt", 'w') as file:
            file.write(writeOnce[0])
        with open(f"data/{semester_offerings_folderName}courseofferings_{course_subject}.txt", 'w') as file:
            file.write(writeOnce[1])

    else:
        print(f'BAD response: {response.status_code}')
    
    
def coursePatternMatchBatch(course_title_hours: str, writeOnce: List) -> str:
    '''
        Attempt* to batch write into file rather than independently write many more times.
        Regex match input string for current course, append polished output into List parameter.

        Parameters:
            course_title_hours (str): contains raw string of courseNum, title, and credit hours.        ex: CS 111.  Program Design I.  3 hours.
            writeOnce (List[str, str]): contains raw strings that we append to at end of function. These strings get batch written to files.
        Returns:
            course_subject (str): Prefix of the courseID. ex: CS, MATH...
    '''

    pattern = re.compile(r"""
        ^([A-Z]+)\s+(\d+)\.                                     # subject and course number ex: 'CS 100.'
        \s+(.+?[.?!])                                           # course title, non-greedy up to next period
        \s+(\d+(?:\s*-\s*\d+|\s+or\s+\d+)?\s*hours?)\.?$        # hour(s): 3, 1-3, or '3 or 4'
    """, re.VERBOSE)

    match = pattern.match(course_title_hours)
    
    if match:
        course_subject = match.group(1)
        course_number = match.group(2)
        course_title = match.group(3).strip()
        course_hours = match.group(4).strip()
        
        course_num = f"{course_subject}___{course_number}"                                          # chose delimiter
        course_hours = (convHourRangeToList(course_hours))
        course_subject = "".join(char for char in course_num if char.isalpha())
        # print(f"Course: {course_num}, Subject: {course_subject}, Hours: {course_hours}")            # for debugging

        # save everything to string buffer in list and only write once to each  .txt file rather than numCourses times
        writeOnce[0] += (f"{course_num}\t{course_hours}\n")
        writeOnce[1] += (f"{course_num}\t0\t0\n")
            
        return course_subject
    else:
        print(f"Error writiting to {course_subject}")
        print(match)
        return ''


"""
import timeit

data = scrapeCatalogFrontPage(UIC_URL)
def benchmarkIngest():
    scrapeCatalogFrontPage(UIC_URL)

def benchmarkBatchSingle():
    csLink = data['Computer Science (CS)']
    writeCourseInfoToFileBatch(csLink)               # testing data point

def benchmarkBatchALL():
    for d in data:
        writeCourseInfoToFileBatch(data[d])

def benchmarkStreamSingle():
    csLink = data['Computer Science (CS)']
    writeCourseInfoToFileStream(csLink)               # testing data point

def benchmarkStreamALL():
    for d in data:
        writeCourseInfoToFileStream(data[d])
"""

if __name__ == "__main__":
    UIC_URL = 'https://catalog.uic.edu/all-course-descriptions/'
    data = scrapeCatalogFrontPage(UIC_URL)
    # csLink = data['Computer Science (CS)']; writeCourseInfoToFileBatch(csLink)               # testing data point
    for d in data:
        # writeCourseInfoToFileBatch(data[d])
        writeCourseInfoToFileStream(data[d])

    '''
    print(f'Single Stream: {timeit.timeit(benchmarkStreamSingle, number=1)}')
    print(f'ALL Stream: {timeit.timeit(benchmarkStreamALL, number=1)}')
    print(f'Single Batch: {timeit.timeit(benchmarkBatchSingle, number=1)}')
    print(f'ALL Batch: {timeit.timeit(benchmarkBatchALL, number=1)}')
    '''