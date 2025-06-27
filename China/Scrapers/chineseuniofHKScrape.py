import json
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re

with open("links.json",'r', encoding="utf-8") as f:
    links = json.load(f)
    url_links = list(links.values())
    uniName = list(links.keys())

url = url_links[5]
uni = uniName[5]

driver = webdriver.Chrome()
driver.get(url)
professors = []

soup = BeautifulSoup(driver.page_source, "html.parser")
faculty_divs = soup.select('div.sptp-member')
print(f"🔎 Found {len(faculty_divs)} faculty divs.")

for idx, div in enumerate(faculty_divs):
    # Get name
    name_div = div.find('div', class_='sptp-member-name')
    name = name_div.find('h2').text.strip() if name_div and name_div.find('h2') else None

    # Get profile link
    a_tag = div.find('a', class_='sptp-member-avatar')
    profile_url = a_tag.get('href') if a_tag else None
    if profile_url and not profile_url.startswith('http'):
        profile_url = "https://www.cse.cuhk.edu.hk" + profile_url

    if name and profile_url:
        try:
            profile_driver = webdriver.Chrome()
            profile_driver.get(profile_url)
            profile_soup = BeautifulSoup(profile_driver.page_source, 'html.parser')
            email = None
            # Find the email in the elementor-widget-container
            containers = profile_soup.find_all('div', class_='elementor-widget-container')
            for container in containers:
                items = container.find_all('li', class_='elementor-icon-list-item')
                for item in items:
                    icon = item.find('i', class_='fas fa-envelope')
                    if icon:
                        text_span = item.find('span', class_='elementor-icon-list-text')
                        if text_span:
                            email_raw = text_span.text.strip()
                            # Remove [] around @ if present
                            email = re.sub(r'\[?@]?', '@', email_raw.replace(' ', ''))
                            break
                if email:
                    break
            if email:
                professors.append({'Name': name, 'Email': email, 'University': uni})
                print(f"✅ [{idx+1}] Name: {name}, Email: {email}")
            else:
                print(f"⚠️  [{idx+1}] No email for {name}, skipping.")
            profile_driver.quit()
        except Exception as e:
            print(f"❌ Error visiting profile for {name}: {e}")
    else:
        print(f"⚠️  [{idx+1}] Missing name or profile link in faculty div.")

# Save results
with open('chprofessors.json', 'a', encoding='utf-8') as f:
    json.dump(professors, f, indent=2, ensure_ascii=False)
print(f"\n💾 Saved {len(professors)} professors with emails to chprofessors.json")
driver.quit()