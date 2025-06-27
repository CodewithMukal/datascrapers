import json
import re
from bs4 import BeautifulSoup
import time
from selenium import webdriver

with open('links.json', 'r') as f:
    links = json.load(f)
    uni_links = list(links["USA"].values())
url = uni_links[9]  
driver = webdriver.Chrome()
driver.get(url)
professors = []

soup = BeautifulSoup(driver.page_source, 'html.parser')
personnel_list = soup.find('ul', class_='personnel-list')
if not personnel_list:
    print("❌ Could not find 'personnel-list' ul.")
else:
    items = personnel_list.find_all('li', recursive=False)
    print(f"🔎 Found {len(items)} personnel list items.")
    for idx, item in enumerate(items):
        anchor = item.find('a')
        name = None
        profile_url = None
        if anchor:
            name_div = anchor.find('div', class_='personnel-list__person-name')
            if name_div and name_div.text.strip():
                name = name_div.text.strip()
            profile_url = anchor.get('href')
            if profile_url and not profile_url.startswith('http'):
                profile_url = 'https://ischool.illinois.edu' + profile_url
        if name and profile_url:
            try:
                profile_driver = webdriver.Chrome()
                profile_driver.get(profile_url)
                profile_soup = BeautifulSoup(profile_driver.page_source, 'html.parser')
                email_tag = profile_soup.find('a', class_='profile__link', href=lambda x: x and x.lower().startswith('mailto:'))
                if email_tag and email_tag['href']:
                    email = email_tag['href'].replace('mailto:', '').strip()
                    professors.append({'Name': name, 'Email': email, 'University': 'University of Illinois'})
                    print(f"✅ [{idx+1}] Name: {name}, Email: {email}")
                else:
                    print(f"⚠️  [{idx+1}] No email for {name}, skipping.")
                profile_driver.quit()
            except Exception as e:
                print(f"❌ Error visiting profile for {name}: {e}")
        else:
            print(f"⚠️  [{idx+1}] Missing name or profile link in personnel list item.")

# Save results
with open('professors.json', 'a', encoding='utf-8') as f:
    json.dump(professors, f, indent=2, ensure_ascii=False)
print(f"\n💾 Saved {len(professors)} professors with emails to professors.json")
driver.quit()