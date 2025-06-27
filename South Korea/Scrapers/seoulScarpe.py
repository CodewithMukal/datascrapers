import json
from selenium import webdriver
import time
from bs4 import BeautifulSoup

with open('links.json','r') as f:
    links = json.load(f)
    uniName = list(links.keys())
    urls = list(links.values())

uni = uniName[0]
driver = webdriver.Chrome()
driver.get(urls[0])
print("✅  Starting extraction.....")

soup = BeautifulSoup(driver.page_source,'html.parser')
professors = []
profs = soup.select('article.group.flex')

if profs:
    print("✅Found list of professor cards! Total number: ",len(profs))

    for i,profInfo in enumerate(profs,1):
        print(f"⏲️ Processing Professor Number {i}")
        name = profInfo.find("span",class_="font-bold").text
        if(name):
            print(f"Name is: {name}")
            mail_link = profInfo.find("a", href= lambda href:href and href.startswith('mailto:'))
            if(mail_link):
                mail = mail_link['href'].replace('mailto:','')
                print(f"Found mail for {name}: {mail}")
                professors.append({"Name":name,"Email":mail,"University":uni})
            else:
                print("❌ No mail found. Skipping... ❕")
                continue
        else:
            print("❌❌No name for this Professor")
            continue
else:
    print("No professors in website!")

print("Now writing in file 🖊️...")
if(len(professors)!=0):
    with open('skprofessors.json','a',encoding='utf-8') as f:
        json.dump(professors,f,indent=2,ensure_ascii=False)
print(f"Done saving {len(professors)} with mails.")

driver.quit()