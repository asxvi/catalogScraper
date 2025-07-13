from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime


def getAllTimes(SUBJECT_URL: str) -> list:
    response = requests.get(SUBJECT_URL)
    if response.status_code == 200:
        dayToTimeMap = {'M': 0, 'T': 24, 'W': 48, 'Th':72, 'F':96}
        returnString = ""
        
        soup = BeautifulSoup(response.content, 'html.parser')
        courses = soup.find_all('div', class_='row course')
        for course in courses:
            listOfTable = []; numTimes = 0
            vals = []; currCourse = course.find('h2').text

            rows = course.find_all('tr')
            header = [th.text.strip() for th in rows[0].find_all('th')]
            for row in rows[1:]:
                for td in row.find_all('td'):
                    # print(td)
                    if td.get('class') is not None:         # handles separators and not good values
                        continue

                    vals.append(td.text.split)
                    vals = [td.text.strip() for td in row.find_all('td')]    
                    listOfTable.append(dict(zip(header, vals)))

            print(listOfTable)
            

            if row['CRN'].isdigit() and len(row['CRN']) == 5:
                print("valid")
            else:
                print('coon')

            continue

            for row in listOfTable:
                if 'Required' in row['CRN']:
                    continue

                print(row)
                continue
                if 'lec' in row['Course Type'].lower():                 # Prof wanted to start simple and later include lab/discus
                    print(row)
                    numTimes += 1

                    daysScheduled = row['Meeting Days']     # the days we meet
                    timeScheduled = row['Start & End Time'] # the time we meet
                    
                    # garb = "11:00 AM - 12:15 PM"
                    # garb = "12:00 PM - 01:50 PM"
                    # start_raw, end_raw = [t.strip() for t in garb.split('-')]

                    start_raw, end_raw = [t.strip() for t in timeScheduled.split('-')]
                    startTimeHM = datetime.strptime(start_raw, "%I:%M %p").strftime("%H:%M")
                    endTimeHM = datetime.strptime(end_raw, "%I:%M %p").strftime("%H:%M")
                    startTimeHour, startTimeMin = startTimeHM.split(':')[0], startTimeHM.split(':')[1]
                    endTimeHour, endTimeMin = endTimeHM.split(':')[0], endTimeHM.split(':')[1]

                    day_pattern = re.compile(r"(Th|M|T|W|F)")
                    days = day_pattern.findall(daysScheduled)

                    
                    # days = ['Th', 'T']
                    if 'Th' in days or 'T' in days:
                        days.sort()
                        
                    # print(f'start: {startTimeHour, startTimeMin}')
                    # print(f'end: {endTimeHour, endTimeMin}')

                    startTime, endTime = 0, 0
                    for d in days:
                        startTime = dayToTimeMap[d] * 60 + int(startTimeHour) * 60 + int(startTimeMin)
                        endTime = dayToTimeMap[d] * 60 + int(endTimeHour) * 60 + int(endTimeMin)
                    

            # break


        

        






if __name__ == '__main__':
    getAllTimes('https://webcs7.osss.uic.edu/schedule-of-classes/static/schedules/fall-2025/CS.html')