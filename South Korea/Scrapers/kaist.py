import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup

with open('links.json','r') as f:
    links = json.load(f)
    uniName = list(links.keys())
    urls = list(links.values())

uni = uniName[1]
driver = webdriver.Chrome()

print("✅  Starting extraction.....")
translated_url = f"https://translate.google.com/translate?sl=ko&tl=en&u={urls[1]}"
driver.get(translated_url)

soup = BeautifulSoup(driver.page_source,'html.parser')
professors = []

titles = soup.find_all("p",class_="line")
if(titles):
    title = titles[0]
    profCards = title.find_next_sibling('ul')
    profInfos = profCards.find_all('li')
    print(f"Found {len(profInfos)} professors.")
    for i,prof in enumerate(profInfos,1):
        print(f"Processing Professor {i}....")
        name = prof.find('p',class_="name").text
        if(name):
            print(f"Found {name}")
        emailP = prof.find('p',class_="text")
        if(emailP):
            print("Found mail container")
            mail = emailP.find('span').text
            if(mail):
                print("Found mail!")
                if(" (at) " in mail):
                    print("Formatting mail...")
                    mail = mail.replace(' (at) ','@')
                print(f"Mail for {name} is {mail}")
                professors.append({"Name":name,"Email":mail,"University":uni})
            else:
                print("No mail found!, Skipping")
                continue
        else:
            print("No mail container found, Skipping")
            continue

print(f"Found {len(professors)} professors")
if(len(professors)!=0):
    with open('skprofessors.json','a',encoding='utf-8') as f:
        print("Wrting Mails!")
        json.dump(professors,f,ensure_ascii=False,indent=2)

driver.quit()