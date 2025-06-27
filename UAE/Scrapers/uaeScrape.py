import json
import time
from selenium import webdriver
from bs4 import BeautifulSoup

with open('links.json','r') as f:
    links = json.load(f)
    urls = list(links.values())
    unis = list(links.keys())

professors = []

url = urls[0]
uni = unis[0]

driver = webdriver.Chrome()
driver.get(url)

soup = BeautifulSoup(driver.page_source,'html.parser')

div = soup.find('div',class_=["accordian_wrapper","tab-content"])

div = div.find('div',id="d13e118-vertab-5")

if(div):
    print("Faculty div found!")
    table = div.find('table',class_="table")
    if(table):
        tr = table.find_all("tr")
        if(tr != []):
            for i,row in enumerate(tr,1):
                if(i==1):continue
                cols = row.find_all("td")
                if(cols):
                    name = (cols[0].text).strip()
                    mail = (cols[2].text).strip()
                    print(f"Name: {name}, Email: {mail}")
                    professors.append({"Name":name,"Email":mail,"University":uni})
                else:
                    print("Cant find cols inside table")
        else:
            print("Table rows couldnt be found")
    else:
        print("Cant find any table")
else:
    print("Couldnt find div")

if(len(professors)!=0):
    with open('uaeprofessors.json','a',encoding='utf-8') as f:
        json.dump(professors,f,indent=2,ensure_ascii=False)
print(f"Done saving {len(professors)} with mails.")