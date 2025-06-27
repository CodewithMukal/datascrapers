import json
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

with open('links.json','r') as f:
    links = json.load(f)
    urls = list(links.values())
    unis = list(links.keys())

professors = []

url = urls[3]
uni = unis[3]

driver = webdriver.Chrome()
driver.get(url)

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)

for i in range(6):
    # Parse current page
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    divs = soup.find_all('div', class_=["field-item", 'even'])
    div = divs[9] if len(divs) > 9 else None

    if div:
        print(f"Found div on page {i+1}")
        profsDiv = div.find('div', class_="view-content")
        if profsDiv:
            profs = profsDiv.find_all('div')
            for prof in profs:
                name = prof.find('div', class_="views-field-title")
                if name:
                    name = name.text.strip()
                    print(f"{name} found!")
                    anchor = prof.find('a')
                    if anchor:
                        link = anchor.get('href')
                        if link:
                            newdriver = webdriver.Chrome()
                            newdriver.get(link)
                            time.sleep(5)
                            newsoup = BeautifulSoup(newdriver.page_source, 'html.parser')
                            cont = newsoup.find('h2', class_="pane-title", string=lambda x: x and x.strip() == "Contact")
                            if cont:
                                maildiv = cont.find_next_sibling()
                                if maildiv:
                                    mail = maildiv.text.strip()
                                    print(f"Email for {name}: {mail}")
                                    professors.append({"Name":name,"Email":mail,"University":uni})
                            newdriver.quit()
    else:
        print(f"No target div on page {i+1}")

    # Don't click next on last iteration
    if i != 5:
        try:
            next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[title="Go to next page"]')))
            next_button.click()
            time.sleep(3)  # allow page to load
        except Exception as e:
            print(f"Failed to click next: {e}")
            break
print(len(uni),"profs found!")

if(len(professors)!=0):
    with open('uaeprofessors.json','a',encoding='utf-8') as f:
        json.dump(professors,f,indent=2,ensure_ascii=False)
print(f"Done saving {len(professors)} with mails.")