import json
from bs4 import BeautifulSoup
from selenium import webdriver

with open('links.json', 'r') as f:
    links = json.load(f)
    uni_links = list(links["USA"].values())
url = uni_links[10]
driver = webdriver.Chrome()
driver.get(url)
professors = []

soup = BeautifulSoup(driver.page_source, 'html.parser')
main_block = soup.find('div', class_='block block-system block-system-main-block')
if main_block:
    content_div = main_block.find('div', class_='content')
else:
    content_div = None
if not content_div:
    print("❌ Could not find 'content' div.")
else:
    prof_divs = content_div.find_all('div', class_='d-flex flex-column')
print(f"🔎 Found {len(prof_divs)} faculty divs in content div.")
for idx, prof_div in enumerate(prof_divs):
    anchor = prof_div.find('a')
    h4 = anchor.find('h4') if anchor else None
    name = None
    profile_url = None
    if h4 and h4.text.strip():
        name = h4.text.strip()
        profile_url = anchor.get('href') if anchor else None
        if profile_url and not profile_url.startswith('http'):
            profile_url = 'https://ai.ucsd.edu' + profile_url
    if name and profile_url:
        try:
            profile_driver = webdriver.Chrome()
            profile_driver.get(profile_url)
            profile_soup = BeautifulSoup(profile_driver.page_source, 'html.parser')
            email_tag = profile_soup.find('a', href=lambda x: x and x.lower().startswith('mailto:'))
            if email_tag and email_tag['href']:
                email = email_tag['href'].replace('mailto:', '').strip()
                professors.append({'Name': name, 'Email': email, 'University': 'University of California'})
                print(f"✅ [{idx+1}] Name: {name}, Email: {email}")
            else:
                print(f"⚠️  [{idx+1}] No email for {name}, skipping.")
            profile_driver.quit()
        except Exception as e:
            print(f"❌ Error visiting profile for {name}: {e}")
    else:
        print(f"⚠️  [{idx+1}] Missing name or profile link in faculty div.")

with open('professors.json', 'a', encoding='utf-8') as f:
    json.dump(professors, f, indent=2, ensure_ascii=False)
print(f"\n💾 Saved {len(professors)} professors with emails to professors.json")
driver.quit()