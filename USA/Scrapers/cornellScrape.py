import json
import time
import requests as re
from bs4 import BeautifulSoup
from selenium import webdriver
import re as regex

with open('links.json', 'r') as f:
    links = json.load(f)
    uni_links = list(links["USA"].values())
url = uni_links[6]  # Cornell University link

driver = webdriver.Chrome()
driver.get(url)
professors = []
soup = BeautifulSoup(driver.page_source, 'html.parser')
print("🔍 Scraping professor emails from:", url)

try:
    view_content = soup.find('div', class_='view-content')
    if not view_content:
        print("❌ Could not find 'view-content' div.")
    else:
        person_divs = view_content.find_all('div', class_='person-listing')
        print(f"🔎 Found {len(person_divs)} person-listing divs.")
        for idx, person in enumerate(person_divs):
            name = None
            email = None
            # Extract name
            h6 = person.find('h6')
            if h6:
                a_name = h6.find('a')
                if a_name and a_name.text.strip():
                    name = a_name.text.strip()
            # Extract email
            a_mail = person.find('a', href=lambda x: x and x.lower().startswith('mailto:'))
            if a_mail and a_mail['href']:
                email = a_mail['href'].replace('mailto:', '').strip()
            if name and email:  # Only add if both name and email exist
                professors.append({'Name': name, 'Email': email, 'University': 'Cornell University'})
                print(f"✅ [{idx+1}] Name: {name}, Email: {email}, University: Cornell University")
            elif name:
                print(f"⚠️  [{idx+1}] No email for {name}, skipping.")
            else:
                print(f"⚠️  [{idx+1}] Missing name in person-listing div.")
    # Save results
    with open('professors.json', 'a', encoding='utf-8') as f:
        json.dump(professors, f, indent=2, ensure_ascii=False)
    print(f"\n💾 Saved {len(professors)} professors with emails to professors.json")
except Exception as e:
    print(f"❌ Error during scraping: {e}")
finally:
    driver.quit()