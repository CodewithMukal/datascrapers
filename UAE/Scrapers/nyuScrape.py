import json
import time
from bs4 import BeautifulSoup
from selenium import webdriver

with open('links.json','r') as f:
    links = json.load(f)
    urls = list(links.values())
    unis = list(links.keys())

professors = []

url = urls[4]
uni = unis[4]

driver = webdriver.Chrome()
driver.get(url)
time.sleep(5)
soup = BeautifulSoup(driver.page_source,'html.parser')

names = soup.find_all(attrs={'itemprop':'name'})
mails = soup.find_all(attrs={'itemprop':'email'})

print(f"{len(names)} name found")
print(f"{len(mails)} name found")

for name,mail in zip(names,mails):
    name = name.text
    mail = mail.text
    print(f"Email for {name} is {mail}")
    professors.append({"Name":name,"Email":mail,"University":uni})

if(len(professors)!=0):
    with open('uaeprofessors.json','a',encoding='utf-8') as f:
        json.dump(professors,f,indent=2,ensure_ascii=False)
print(f"Done saving {len(professors)} with mails.")
