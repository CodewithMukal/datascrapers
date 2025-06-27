import json
from selenium import webdriver
from bs4 import BeautifulSoup

with open('links.json', 'r') as f:
    links = json.load(f)
    uni_links = list(links["USA"].values())
url = uni_links[8]
driver = webdriver.Chrome()
driver.get(url)
professors = []

soup = BeautifulSoup(driver.page_source, 'html.parser')
faculty_cards = soup.find('div', id='faculty-cards')
if not faculty_cards:
    print("❌ Could not find 'faculty-cards' div.")
else:
    card_divs = faculty_cards.find_all('div', recursive=False)
    print(f"🔎 Found {len(card_divs)} faculty card divs.")
    for idx, card in enumerate(card_divs):
        h2 = card.find('h2')
        name = None
        profile_url = None
        if h2:
            a_tag = h2.find('a')
            if a_tag and a_tag.text.strip() and a_tag.get('href'):
                name = a_tag.text.strip()
                profile_url = a_tag['href']
                if not profile_url.startswith('http'):
                    profile_url = 'https://www.ml.cmu.edu' + profile_url
        if name and profile_url:
            try:
                profile_driver = webdriver.Chrome()
                profile_driver.get(profile_url)
                profile_soup = BeautifulSoup(profile_driver.page_source, 'html.parser')
                email_tag = profile_soup.find('a', href=lambda x: x and x.lower().startswith('mailto:'))
                if email_tag and email_tag['href']:
                    email = email_tag['href'].replace('mailto:', '').strip()
                    professors.append({'Name': name, 'Email': email, 'University': 'Carnegie Mellon University'})
                    print(f"✅ [{idx+1}] Name: {name}, Email: {email}")
                else:
                    print(f"⚠️  [{idx+1}] No email for {name}, skipping.")
                profile_driver.quit()
            except Exception as e:
                print(f"❌ Error visiting profile for {name}: {e}")
        else:
            print(f"⚠️  [{idx+1}] Missing name or profile link in faculty card.")

with open('professors.json', 'a', encoding='utf-8') as f:
    json.dump(professors, f, indent=2, ensure_ascii=False)
print(f"\n💾 Saved {len(professors)} professors with emails to professors.json")
driver.quit()