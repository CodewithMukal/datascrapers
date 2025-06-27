import json
from selenium import webdriver
from bs4 import BeautifulSoup
import requests as re

with open('links.json','r') as f:
    links = json.load(f)
    "key is the name of uni and value is link, i want to make an array of links"
    uni_links = list(links["USA"].values())

# FOR 0th link
driver = webdriver.Chrome()
driver.get(uni_links[0])
soup = BeautifulSoup(driver.page_source, 'html.parser')
professors = []
for entry in soup.find_all('div', class_='people-entry'):
    name = entry.find('h5').get_text(strip=True)
    email_tag = entry.find('ul').find('a', href=True)
    if email_tag and 'mailto:' in email_tag['href']:
        email = email_tag['href'].replace('mailto:', '')
        professors.append({
            "Name": name,
            "Email": email,
            "University": "MIT"
        })
with open('professors.json', 'w') as f:
    json.dump(professors, f, indent=4)
driver.quit()

url = uni_links[1]
driver.get(url)

professors = []

