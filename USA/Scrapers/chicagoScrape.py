import json
import re
from bs4 import BeautifulSoup
import time
from selenium import webdriver

with open('links.json', 'r') as f:
    links = json.load(f)
    uni_links = list(links["USA"].values())
url = uni_links[3] 
driver = webdriver.Chrome()
driver.get(url)
professors = []

soup = BeautifulSoup(driver.page_source, 'html.parser')
print("🔍 Scraping professor emails from:", url)
print("✅ Successfully loaded the page")
results_div = soup.find('div', class_='results')
if results_div:
    print("✅ Found results div")
    card_entries = results_div.find_all('div', class_='card__content')
    print(f"🔢 Found {len(card_entries)} card entries in results div")
    for idx, entry in enumerate(card_entries, 1):
        print(f"➡️ Processing card {idx}")
        name_tag = entry.find('h3', class_='card__title')
        if not name_tag:
            print(f"⚠️ No name found in card {idx}")
            continue
        name = name_tag.get_text(strip=True)

        parent_card = entry.find_parent('div', class_='card')
        link_tag = None
        if parent_card:
            link_tag = parent_card.find('a', href=True)
        if not link_tag:
            print(f"⚠️ No profile link found for {name}")
            continue
        profile_url = link_tag['href']
        print(f"🔗 Visiting profile page: {profile_url}")
        driver.get(profile_url)
        time.sleep(2) 
        profile_soup = BeautifulSoup(driver.page_source, 'html.parser')
        email_tag = profile_soup.find('a', href=re.compile(r'mailto:'))
        if email_tag:
            email = email_tag['href'].replace('mailto:', '')
            print(f"✅ Found email for {name}: {email}")
            professors.append({
                "Name": name,
                "Email": email,
                "University": "University of Chicago"
            })
        else:
            print(f"❌ No email found for {name} at {profile_url}")
else:
    print("❌ Results div not found on the page!")
print(f"🧑‍🏫 Total professors with emails found: {len(professors)}")
with open('professors.json','a') as f:
    json.dump(professors, f, indent=4)
driver.quit()
print("✅ Scraping completed and data saved to professors.json")