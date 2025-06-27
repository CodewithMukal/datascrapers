import json
from selenium import webdriver
from bs4 import BeautifulSoup

url_links = None
uniName = None

with open("links.json",'r') as f:
    links = json.load(f)
    url_links = list(links.values())
    uniName = list(links.keys())

url = url_links[1]
uni = uniName[1]

driver = webdriver.Chrome()
driver.get(url)
professors = []

soup = BeautifulSoup(driver.page_source, "html.parser")

# Find the <p> tag with the specific content
p_tag = soup.find('p', string="Key Laboratory of Artificial Intelligence, Ministry of Education")
if not p_tag:
    print("❌ Could not find the target <p> tag.")
else:
    faculty_div = p_tag.find_next_sibling('div', class_='Faculty')
    if not faculty_div:
        print("❌ Could not find the Faculty div after the <p> tag.")
    else:
        lis = faculty_div.find_all('li')
        print(f"🔎 Found {len(lis)} faculty li's.")
        for idx, li in enumerate(lis):
            a_tag = li.find('a')
            if a_tag and a_tag.text.strip() and a_tag.get('href'):
                name = a_tag.text.strip()
                profile_url = a_tag['href']
                if not profile_url.startswith('http'):
                    profile_url = url.rstrip('/') + '/' + profile_url.lstrip('/')
                try:
                    profile_driver = webdriver.Chrome()
                    profile_driver.get(profile_url)
                    profile_soup = BeautifulSoup(profile_driver.page_source, 'html.parser')
                    email_tag = profile_soup.find('a', href=lambda x: x and x.lower().startswith('mailto:'))
                    if email_tag and email_tag['href']:
                        email = email_tag['href'].replace('mailto:', '').strip()
                        professors.append({'Name': name, 'Email': email, 'University': uni})
                        print(f"✅ [{idx+1}] Name: {name}, Email: {email}")
                    else:
                        print(f"⚠️  [{idx+1}] No email for {name}, skipping.")
                    profile_driver.quit()
                except Exception as e:
                    print(f"❌ Error visiting profile for {name}: {e}")
            else:
                print(f"⚠️  [{idx+1}] Missing name or profile link in li.")

# Save results
with open('chprofessors.json', 'a', encoding='utf-8') as f:
    json.dump(professors, f, indent=2, ensure_ascii=False)
print(f"\n💾 Saved {len(professors)} professors with emails to chprofessors.json")
driver.quit()