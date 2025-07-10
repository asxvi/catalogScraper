from bs4 import BeautifulSoup
import requests
import string
from typing import List
import os


def getAllTimes(SUBJECT_URL: str) -> list:
    response = requests.get(SUBJECT_URL)
    if response.status_code == 200:
        returnString = ""
        

        soup = BeautifulSoup(response.content, 'html.parser')
        courses = soup.find_all('div', class_='row course')
        for course in courses:
            listOfTable = []
            currCourse = course.find('h2').text

            rows = course.find_all('tr')
            header = [th.text.strip() for th in rows[0].find_all('th')]

            for row in rows[1:]:
                vals = [td.text.strip() for td in row.find_all('td')]    
                listOfTable.append(dict(zip(header, vals)))

            for row in listOfTable:
                if 'Required' in row['CRN']:
                    continue
                if 'lab' in row['Course Type'].lower():
                    print(row)
                
            
            break
        

        






if __name__ == '__main__':
    getAllTimes('https://webcs7.osss.uic.edu/schedule-of-classes/static/schedules/fall-2025/CS.html')