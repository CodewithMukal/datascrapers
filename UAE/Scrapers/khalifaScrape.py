import json
import time
from bs4 import BeautifulSoup
from selenium import webdriver

with open('links.json','r') as f:
    links = json.load(f)
    urls = list(links.values())
    unis = list(links.keys())

professors = []

url = urls[1]
uni = unis[1]

driver = webdriver.Chrome()
driver.get(url)
time.sleep(5)
soup = BeautifulSoup(driver.page_source,'html.parser')

blocks = soup.find_all('div',class_="blks")
print(f"{len(blocks)} blks found")
for blks in blocks:
    block = blks.find_all('div',class_="blk")
    for blk in block:
        name = blk.find("span",class_=['name','r'])
        email = blk.find('span',class_="email")
        if(name,email):
            name,email = name.text,email.text
            print(f"Found email for {name}: {email}")
            professors.append({"Name":name,"Email":email,"University":uni})

if(len(professors)!=0):
    with open('uaeprofessors.json','a',encoding='utf-8') as f:
        json.dump(professors,f,indent=2,ensure_ascii=False)
print(f"Done saving {len(professors)} with mails.")