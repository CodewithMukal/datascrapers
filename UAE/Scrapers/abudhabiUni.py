import json
import time
from bs4 import BeautifulSoup
from selenium import webdriver

with open('links.json','r') as f:
    links = json.load(f)
    urls = list(links.values())
    unis = list(links.keys())

professors = []

url = "https://www.adu.ac.ae/study/colleges/college-of-engineering/Faculty/"
uni = "Abhu Dhabi University"

driver = webdriver.Chrome()
driver.get(url)
time.sleep(10)
soup = BeautifulSoup(driver.page_source,'html.parser')

profsDiv = soup.find('div',attrs={"data-cat":"Computer Science and Information Technology"})
if(profsDiv):
    print("Found profs div")
outerdiv = profsDiv.find('div')
if(outerdiv): print("Outer div found")
profs = outerdiv.find_all('div',class_="faculty-holder")
if(profs!=[]):
    print("Length of profs",len(profs))
    
for prof in profs:
    name = prof.find('h4')
    if(name):
        name = name.text
        mailDiv = prof.find('div',class_="faculty-info")
        if(mailDiv):
            mail = mailDiv.find('a')
            if(mail):
                mail = mail.text
                print(f"Email for {name}:{mail}")
                professors.append({"Name":name,"Email":mail,"University":uni})
            else:
                print("cant find mail")
    else:
        print("cant find name")

if(len(professors)!=0):
    with open('uaeprofessors.json','a',encoding='utf-8') as f:
        json.dump(professors,f,indent=2,ensure_ascii=False)
print(f"Done saving {len(professors)} with mails.")