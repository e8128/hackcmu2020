
from bs4 import BeautifulSoup
import requests

"""
{
    course number: {
        'sections': [{}], <-- each entry is a dictionary containing the fields below (for recitations)
        'Course': "", <-- course number
        'Title': "", <-- rest are for lecture, check for None before manipulating values
        'Units': "",
        'Lec/Sec': "",
        'Days': "",
        'Begin': "",
        'End': "",
        'Bldg/Room': "",
        'Location': "",
        'Instructor(s)': ""
    }
}
"""


def parseWebsite():
    r = requests.get("https://enr-apps.as.cmu.edu/assets/SOC/sched_layout_fall.htm")
    soup = BeautifulSoup(r.text, 'html.parser')
    table = soup.find_all('tr')
    if (len(table) < 2):
        print("No courses found")
        return None
    labels = table[1]
    courses = table[2:]
    courseDict = {}
    # Creating the indices associated with course attributes
    courseLabels = [label.b.string for label in labels]
    # Creating the dictionary mapping the course number to dictionary mapping fields to values
    i = 0
    while i < len(courses):
        course = courses[i].find_all('td')
        if (course[0].b):
            # Filter Discipline name
            i += 1
            continue
        # course number
        d = dict()
        d['sections'] = []
        for j in range(min(len(courseLabels), len(course))):
            label = courseLabels[j]
            # Really bad solution for 11411
            if (label == 'Location' and len(course[j].string) <= 5):
                d[label] = 'Pittsburgh, Pennsylvania'
            else:
                d[label] = course[j].string
        while (i + 1 < len(courses) and courses[i+1].find_all('td')[0].string == '\xa0'):
            dsub = dict()
            recitation = courses[i+1].find_all('td')
            for k in range(min(len(recitation), len(courseLabels))):
                l = courseLabels[k]
                dsub[l] = recitation[k].string
            d['sections'].append(dsub)
            i += 1
        courseDict[course[0].string] = d
        i += 1
    return courseDict


if __name__ == '__main__':
    print(parseWebsite())