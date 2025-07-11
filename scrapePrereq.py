from bs4 import BeautifulSoup
import requests
import re
import os


# BASE_SPRING_URL = "https://webcs7.osss.uic.edu/schedule-of-classes/static/schedules/spring-2025/"
BASE_SPRING_URL = "https://webcs7.osss.uic.edu/schedule-of-classes/static/schedules/fall-2025/CS.html"


def scrapeStage3(links) -> dict:
    '''
        Uses helper functions: scrapeCatalogFrontPage(), and writeCourseInfoToFileBatch() to 
        - Write to CH file all subjects the number of credit hours they take
        - Write to semester offerings file default values: COURSE 0 0 (for later use)

        Parameters:
            UIC_URL (str): UIC catalog homepage. Only used in part 1
        Returns:
            data (dict {str: str}): On successful exit. Print to console and return dict of direct links 
    '''

    for subject in links:
        getPrerequisites(links[subject])                       # use Batch and not Stream function

    print("Successfully wrote to CHdata and offeringsData")

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