import json
from selenium import webdriver
import requests
import re
from bs4 import BeautifulSoup
import time
with open('links.json', 'r') as f:
    links = json.load(f)
    uni_links = list(links["USA"].values())

url = uni_links[5]  # Yale University link
driver = webdriver.Chrome()
driver.get(url)
professors = []
soup = BeautifulSoup(driver.page_source, 'html.parser')

print("🔍 Scraping professor emails from:", url)
print("✅ Successfully loaded the page")
faculty_div = soup.find('div', id='artificial-intelligence-and-machine-learning')
if faculty_div:
    print("✅ Found faculty div")
    member_list = faculty_div.find('div', class_='faculty-member-list')
    if member_list:
        print(f"🔢 Found {len(member_list.find_all('a'))} faculty members in the list")
        for idx, entry in enumerate(member_list.find_all('a'), 1):
            print(f"➡️ Processing entry {idx}")
            profile_url = entry['href']
            print(f"🔗 Visiting profile page: {profile_url}")
            driver.get(profile_url)
            time.sleep(2)  # Wait for the page to load
            profile_soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            name_tag = profile_soup.find('h1')
            if name_tag:
                name = name_tag.get_text(strip=True)
                email_tag = profile_soup.find('a', class_='arrow-link', href=re.compile(r'mailto:'))
                if email_tag:
                    email = email_tag['href'].replace('mailto:', '')
                    print(f"✅ Found email for {name}: {email}")
                    professors.append({
                        "Name": name,
                        "Email": email,
                        "University": "Yale University"
                    })
                else:
                    print(f"❌ No email found for {name} at {profile_url}")
            else:
                print(f"⚠️ No name found in profile page for {profile_url}")
    else:
        print("❌ Faculty member list not found!")
else:
    print("❌ Faculty div not found on the page!")

print(f"🧑‍🏫 Total professors with emails found: {len(professors)}")
with open('professors.json', 'a') as f:
    json.dump(professors, f, indent=4)