import json
import time
import requests as re
from bs4 import BeautifulSoup
from selenium import webdriver

with open('links.json', 'r') as f:
    links = json.load(f)
    uni_links = list(links["USA"].values())

url = uni_links[2]
driver = webdriver.Chrome()
driver.get(url)
professors = []
soup = BeautifulSoup(driver.page_source, 'html.parser')

print("🔍 Scraping professor emails from:", url)
print("✅ Successfully loaded the page")
print("📊 Total entries found:", len(soup.find_all('div', class_='views-row')))
for entry in soup.find_all('div', class_='views-row'):
    name_tag = entry.find('h2', class_='person__detailed-name')
    if name_tag:
        name = name_tag.get_text(strip=True)
        email_tag = entry.find('div', class_='person__email').find('a', href=True)
        if email_tag and 'mailto:' in email_tag['href']:
            email = email_tag['href'].replace('mailto:', '')
            professors.append({
                "Name": name,
                "Email": email,
                "University": "Harvard University"
            })
print(f"📊 Found {len(professors)} professors with emails")
with open('harvard_professors.json', 'w') as f:
    json.dump(professors, f, indent=4)