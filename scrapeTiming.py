from bs4 import BeautifulSoup
import requests
from typing
import re
from datetime import datetime


def getAllTimes(SUBJECT_URL: str) -> list:
    response = requests.get(SUBJECT_URL)
    if response.status_code == 200:
        dayToTimeMap = {'M': 1, 'T': 2, 'W': 3, 'Th':4, 'F':5}
        returnString = ""
        
        soup = BeautifulSoup(response.content, 'html.parser')
        courses = soup.find_all('div', class_='row course')
        for course in courses:
            listOfTable = []; numTimes = 0
            currCourse = course.find('h2').text

            rows = course.find_all('tr')
            header = [th.text.strip() for th in rows[0].find_all('th')]

            for row in rows[1:]:
                vals = [td.text.strip() for td in row.find_all('td')]    
                listOfTable.append(dict(zip(header, vals)))

            for row in listOfTable:
                if 'Required' in row['CRN']:
                    continue
                if 'lec' in row['Course Type'].lower():
                    print(row)
                    numTimes += 1

                    daysScheduled = row['Meeting Days']     # the days we meet
                    timeScheduled = row['Start & End Time'] # the time we meet
                    addRem = 0
                    
                    # garb = "12:00 PM - 01:50 PM"
                    # start_raw, end_raw = [t.strip() for t in garb.split('-')]
                    start_raw, end_raw = [t.strip() for t in timeScheduled.split('-')]
                    intime = datetime.strptime(start_raw, "%I:%M %p").strftime("%H:%M")
                    outtime = datetime.strptime(end_raw, "%I:%M %p").strftime("%H:%M")

                    print(intime, outtime)
                    # for i, t in enumerate(timeScheduled.split()):
                    #     if 'AM' in t:    
                    #         # print(timeScheduled.split()[i-1])
                    #         intime = (datetime.strptime(timeScheduled.split()[i-1], "%I:%M %p").strftime("%H:%M"))
                    #         outtime = 
                    #         # print(i)

                    day_pattern = re.compile(r"(Th|M|T|W|F)")
                    days = day_pattern.findall(daysScheduled)
                    # for d in days:
                        

            break


        

        






if __name__ == '__main__':
    getAllTimes('https://webcs7.osss.uic.edu/schedule-of-classes/static/schedules/fall-2025/CS.html')