def parseWebsite():
    from bs4 import BeautifulSoup
    import requests
    r = requests.get("https://enr-apps.as.cmu.edu/assets/SOC/sched_layout_fall.htm")
    soup = BeautifulSoup(r.text, 'html.parser')
    print(soup.find('table'))
    return
    table = soup.find('table').find_all('tr')
    if (len(table) < 2):
        print("No courses found")
        return None
    labels = table[1]
    courses = table[2:]
    courseDict = {}
    # Creating the indices associated with course attributes
    courseLabels = [label.b.string for label in labels]
    print(courseLabels)
    # Creating the dictionary mapping the course number to dictionary mapping fields to values
    i = 0
    print(courses)
    while i < len(courses):
        course = courses[i].find_all('td')
        if (course[0].b is not None):
            # Filter Discipline name
            i += 1
        


if __name__ == '__main__':
    parseWebsite()