import json
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

with open('links.json','r') as f:
    links = json.load(f)
    uniName = list(links.keys())
    urls = list(links.values())

uni = uniName[2]
driver = webdriver.Chrome()
driver.get(urls[2])
professors = []

soup = BeautifulSoup(driver.page_source,'html.parser')

div = soup.find(class_="pro_list")

if(div):
    print("Found div containing profs")
    for j in range(5):
        profCards = div.find_all('div')
        if(profCards):
            print(f"Found {len(profCards)}")
            for i,prof in enumerate(profCards,1):
                name = prof.find('dt')
                if(name): name = name.text
                if(name != None):
                    mail = ((prof.find_all('dd')))
                    if(mail): mail = mail[0].text
                    print(f"Found mail of {name}: {mail}")
                    professors.append({"Name":name,"Email":mail,"University":uni})
                else:
                    print("Not found")
                    continue
        print(f"Completed page {j+1} going to next")
        try:
            nextButton = driver.find_element(By.CLASS_NAME,"next")
        except:
            break
    print("All pages done!")
print("Writting in file now")

if(len(professors)!=0):
    with open('skprofessors.json','a',encoding="utf-8") as f:
        json.dump(professors,f,indent=2,ensure_ascii=False)

driver.quit()