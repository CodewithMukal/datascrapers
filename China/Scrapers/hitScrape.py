import json
from bs4 import BeautifulSoup
from selenium import webdriver
import time

# Load keywords
with open("ml_ai_keywords.txt", "r", encoding="utf-8") as f:
    keywords = [line.strip() for line in f]

# Load links and university names
with open("links.json",'r', encoding="utf-8") as f:
    links = json.load(f)
    url_links = list(links.values())
    uniName = list(links.keys())

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

driver = webdriver.Chrome()
url = url_links[4]
uni = uniName[4]
driver.get(url)
professors = []

while True:
    time.sleep(2)  # Wait for page to load
    soup = BeautifulSoup(driver.page_source, "html.parser")
    faculty_divs = soup.find_all('div', class_='tabscon-li')
    print(f"🔎 Found {len(faculty_divs)} faculty divs.")

    for idx, div in enumerate(faculty_divs):
        a_tag = div.find('a')
        name = None
        profile_url = None
        if a_tag:
            name_div = a_tag.find('div', class_='tabscon-name')
            if name_div and name_div.text.strip():
                name = name_div.text.strip()
            profile_url = a_tag.get('href')
        if name and profile_url:
            try:
                profile_driver = webdriver.Chrome()
                profile_driver.get(profile_url)
                profile_soup = BeautifulSoup(profile_driver.page_source, 'html.parser')
                email = None
                for li in profile_soup.find_all('li'):
                    em = li.find('em')
                    span = li.find('span', class_='user-discipline')
                    if em and span and 'emai' in em.text.lower() and '@' in span.text:
                        email = span.text.strip()
                        break
                if email:
                    professors.append({'Name': name, 'Email': email, 'University': uni})
                    print(f"✅ Name: {name}, Email: {email}")
                else:
                    print(f"⚠️  No email for {name}, skipping.")
                profile_driver.quit()
            except Exception as e:
                print(f"❌ Error visiting profile for {name}: {e}")
        else:
            print(f"⚠️  Missing name or profile link in faculty div.")

    # Try to find and click the Next button
    try:
        next_button = driver.find_element(By.LINK_TEXT, "Next")
        next_button.click()
        print("➡️  Clicked Next page.")
    except NoSuchElementException:
        print("No more pages or Next button not found.")
        break

# Save results
with open('chprofessors.json', 'a', encoding='utf-8') as f:
    json.dump(professors, f, indent=2, ensure_ascii=False)
print(f"\n💾 Saved {len(professors)} professors with emails to chprofessors.json")
driver.quit()