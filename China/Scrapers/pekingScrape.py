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

url = url_links[3]
uni = uniName[3]

driver = webdriver.Chrome()
driver.get(url)
professors = []

while True:
    time.sleep(2)  # Wait for page to load if paginated
    soup = BeautifulSoup(driver.page_source, "html.parser")
    divs = soup.find_all('div', class_='ltjs_text')
    for div in divs:
        # Name
        h3 = div.find('h3')
        name = h3.text.strip() if h3 else None

        # Find all dd tags and look for Research Field and E-mail
        research_field = None
        email = None
        for dd in div.find_all('dd'):
            b = dd.find('b')
            if b:
                label = b.text.strip().replace('：', '').replace(':', '')
                content = dd.get_text().replace(b.text, '').strip()
                if label.lower() == 'research field':
                    research_field = content
                if label.lower() == 'e-mail':
                    email = content

        # Check if research field matches any keyword
        if name and email and research_field:
            for kw in keywords:
                if kw.lower() in research_field.lower():
                    professors.append({'Name': name, 'Email': email, 'University': uni})
                    print(f"✅ Name: {name}, Email: {email}, Research Field: {research_field}")
                    break

    # Pagination: Try to click the "Next" button if it exists
    try:
        next_link = driver.find_element("link text", "Next")
        next_link.click()
    except Exception:
        print("No more pages or no Next button found.")
        break

# Save results
with open('chprofessors.json', 'a', encoding='utf-8') as f:
    json.dump(professors, f, indent=2, ensure_ascii=False)
print(f"\n💾 Saved {len(professors)} professors with emails to chprofessors.json")
driver.quit()