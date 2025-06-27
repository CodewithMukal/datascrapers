import json
from selenium import webdriver
from bs4 import BeautifulSoup

url_links = None
uniName = None

with open("links.json",'r') as f:
    links = json.load(f)
    url_links = list(links.values())
    uniName = list(links.keys())

url = url_links[2]
uni = uniName[2]

driver = webdriver.Chrome()
driver.get(url)
professors = []

soup = BeautifulSoup(driver.page_source, "html.parser")

# ...existing code...

ul = soup.find('ul', class_='wp_article_list')
if not ul:
    print("❌ Could not find ul with class 'wp_article_list'.")
else:
    lis = ul.find_all('li')
    print(f"🔎 Found {len(lis)} li's in the article list.")
    for idx, li in enumerate(lis):
        name = None
        profile_url = None
        span = li.find('span', class_='Article_Title')
        if span:
            a = span.find('a')
            if a and a.text.strip() and a.get('href'):
                name = a.text.strip()
                profile_url = a['href']
                if not profile_url.startswith('http'):
                    profile_url = url.rstrip('/') + '/' + profile_url.lstrip('/')
        if name and profile_url:
            try:
                profile_driver = webdriver.Chrome()
                profile_driver.get(profile_url)
                profile_soup = BeautifulSoup(profile_driver.page_source, 'html.parser')
                email = None
                # Only: li with class email and label E-mail
                li_email = profile_soup.find('li', class_='email')
                email = None
                if li_email:
                    label = li_email.find('label')
                    if label and 'email' in label.text.lower().replace('-', '').replace(' ', ''):
                        # Remove the label text from li_email's text to get the email
                        email_candidate = li_email.get_text().replace(label.text, '').strip()
                        if '@' in email_candidate:
                            email = email_candidate
                if email:
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