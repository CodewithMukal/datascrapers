import json
from selenium import webdriver
from bs4 import BeautifulSoup

with open('links.json', 'r') as f:
    links = json.load(f)
    uni_links = list(links["USA"].values())
url = uni_links[7]
driver = webdriver.Chrome()
driver.get(url)
professors = []

soup = BeautifulSoup(driver.page_source, 'html.parser')
people_lists = soup.find('div', class_='people_lists')
if not people_lists:
    print("❌ Could not find 'people_lists' div.")
else:
    person_divs = people_lists.find_all('div', recursive=False)
    print(f"🔎 Found {len(person_divs)} person divs.")
    for idx, person in enumerate(person_divs):
        # Extract name
        name_tag = person.find('p', class_='eecs_person_name')
        name = None
        if name_tag and name_tag.text.strip():
            raw_name = name_tag.text.strip()
            if ',' in raw_name:
                last, first = [x.strip() for x in raw_name.split(',', 1)]
                name = f"{first} {last}"
            else:
                name = raw_name
        # Extract email
        email_tag = person.find('a', class_='person_email')
        email = email_tag.text.strip() if email_tag and email_tag.text else None
        if name and email:
            professors.append({'Name': name, 'Email': email, 'University': 'University of Michigan'})
            print(f"✅ [{idx+1}] Name: {name}, Email: {email}")
        elif name:
            print(f"⚠️  [{idx+1}] No email for {name}, skipping.")
        else:
            print(f"⚠️  [{idx+1}] Missing name in person div.")

# Save results
with open('professors.json', 'a', encoding='utf-8') as f:
    json.dump(professors, f, indent=2, ensure_ascii=False)
print(f"\n💾 Saved {len(professors)} professors with emails to professors.json")
driver.quit()