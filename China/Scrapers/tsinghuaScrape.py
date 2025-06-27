import json
from selenium import webdriver
from bs4 import BeautifulSoup

url_links = None
uniName = None

with open("links.json",'r') as f:
    links = json.load(f)
    url_links = list(links.values())
    uniName = list(links.keys())

url = url_links[0]
uni = uniName[0]

driver = webdriver.Chrome()
driver.get(url)
professors = []

soup = BeautifulSoup(driver.page_source, "html.parser")

# ...existing code...

people_div = soup.find('div', class_='people01-nr')
if not people_div:
    print("❌ Could not find 'people01-nr' div.")
else:
    dls = people_div.find_all('dl')
    if len(dls) < 4:
        print("❌ Less than 4 dl tags found.")
    else:
        target_dl = dls[3]
        uls = target_dl.find_all('ul', class_='clear')
        print(f"🔎 Found {len(uls)} ul.clear in 4th dl.")
        for ul in uls:
            lis = ul.find_all('li')
            for li in lis:
                # Name
                name = None
                name_tag = li.find('div', class_='text')
                if name_tag:
                    h2 = name_tag.find('h2')
                    if h2:
                        a = h2.find('a')
                        if a and a.text.strip():
                            name = a.text.strip()
                # Email
                email = None
                p_tags = li.find_all('p')
                if len(p_tags) >= 3:
                    email_raw = p_tags[2].text.strip()
                    # Replace " AT " and " dot " with "@" and "."
                    email = email_raw.replace(" AT ", "@").replace(" dot ", ".")
                if name and email:
                    professors.append({'Name': name, 'Email': email, 'University': uni})
                    print(f"✅ Name: {name}, Email: {email}")
                else:
                    print(f"⚠️  Missing name or email in li.")

# Save results
with open('chprofessors.json', 'a', encoding='utf-8') as f:
    json.dump(professors, f, indent=2, ensure_ascii=False)
print(f"\n💾 Saved {len(professors)} professors with emails to chprofessors.json")
driver.quit()