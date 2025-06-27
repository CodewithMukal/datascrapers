import json
import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver

with open('links.json', 'r') as f:
    links = json.load(f)
    uni_links = list(links["USA"].values())

url = uni_links[4]  # Princeton University link
driver = webdriver.Chrome()
driver.get(url)
professors = []
soup = BeautifulSoup(driver.page_source, 'html.parser')

print("🔍 Scraping professor emails from:", url)
print("✅ Successfully loaded the page")
people_div = soup.find('div', class_='people')
if people_div:
    print("✅ Found people div")
    li_entries = people_div.find_all('li')
    print(f"🔢 Found {len(li_entries)} professor entries in people div")
    for idx, entry in enumerate(li_entries, 1):
        print(f"➡️ Processing entry {idx}")
        name_tag = entry.find('h3', class_='custom_card__heading')
        if not name_tag:
            print(f"⚠️ No name found in entry {idx}")
            continue
        name = name_tag.get_text(strip=True)

        link_tag = name_tag.find('a', href=True)
        if not link_tag:
            print(f"⚠️ No profile link found for {name}")
            continue
        profile_url = link_tag['href']
        print(f"🔗 Visiting profile page: {profile_url}")
        
        driver.get("https://www.cs.princeton.edu"+profile_url)
        time.sleep(2)  # Wait for the page to load
        profile_soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        email_tag = profile_soup.find('a', href=re.compile(r'mailto:'))
        if email_tag:
            email = email_tag['href'].replace('mailto:', '')
            print(f"✅ Found email for {name}: {email}")
            professors.append({
                "Name": name,
                "Email": email,
                "University": "Princeton University"
            })
        else:
            print(f"❌ No email found for {name} at {profile_url}")

else:
    print("❌ People div not found on the page!")
print(f"🧑‍🏫 Total professors with emails found: {len(professors)}")
with open('professors.json', 'a') as f:
    json.dump(professors, f, indent=4)

# Close the Selenium driver
driver.quit()