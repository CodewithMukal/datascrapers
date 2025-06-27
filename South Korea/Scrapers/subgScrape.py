import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

with open('links.json','r') as f:
    links = json.load(f)
    uniName = list(links.keys())
    urls = list(links.values())

uni = uniName[3]
driver = webdriver.Chrome()
driver.get(urls[3])
professors = []

soup = BeautifulSoup(driver.page_source,'html.parser')

allProfs = soup.find_all('div',class_="faculty-info-box")

def convert_name_format(name):
    if ',' in name:
        last, first = name.split(',', 1)
        return f"{first.strip()} {last.strip()}"
    return  # fallback if no comma found

if(allProfs):
    print(f"Found {len(allProfs)} Professors!")
    for i,prof in enumerate(allProfs,1):
        print(f"PROF {i}")
        dd = prof.find_all('dd')
        if(dd):
            name = dd[0]
            li = name.find_all("li")
            if(li):
                nameLI = li[1]
                name = nameLI.find('span')
                if(name):
                    name = name.text
                    name = convert_name_format(name)
                    print(name)
                    mailDD = dd[1]
                    mail = mailDD.find('li',class_="mail")
                    if(mail):
                        mail = mail.text
                        print(f"Mail for {name} is {mail}")
                        professors.append({"Name":name,"Email":mail,"University":uni})
                    else:
                        print("Mail not found")
                else:
                    print("Name not found")

print("Done")
if(len(professors)!=0):
    with open('skprofessors.json','a',encoding='utf-8') as f:
        json.dump(professors,f,indent=2,ensure_ascii=False)
print(f"Done saving {len(professors)} with mails.")   
driver.quit()