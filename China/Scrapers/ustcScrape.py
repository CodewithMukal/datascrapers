import json
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re

with open("links.json",'r', encoding="utf-8") as f:
    links = json.load(f)
    url_links = list(links.values())
    uniName = list(links.keys())

url = url_links[6]
uni = uniName[6]

driver = webdriver.Chrome()
driver.get(url)
professors = []
time.sleep(2)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# Extract all name spans
name_spans = soup.find_all('span', style=lambda v: v and 'font-size:20px' in v and 'color:#002060' in v)

# Build a list of (name, parent) tuples to help map names to emails
name_blocks = []
for span in name_spans:
    parent = span.find_parent('p')
    if not parent:
        parent = span.parent
    name_blocks.append({'name': span.get_text(strip=True), 'block': parent})

# Extract all email <p> blocks
email_blocks = []
# ...existing code...

# Iterate through all <p> tags in order, track last seen name
professors = []
last_name = None
for p in soup.find_all('p'):
    # Check for name span
    name_span = p.find('span', style=lambda v: v and 'font-size:20px' in v and 'color:#002060' in v)
    if name_span:
        last_name = name_span.get_text(strip=True)
    # Check for email block
    spans = p.find_all('span')
    if len(spans) == 2 and spans[0].get_text(strip=True).lower().startswith('e-mail'):
        email = spans[1].get_text(strip=True)
        if last_name and email:
            professors.append({
                'Name': last_name,
                'Email': email,
                'University': uni
            })

# ...rest of your code for saving...

# Map each email to the closest previous name
# professors = []
# for email_block in email_blocks:
#     email = email_block['email']
#     email_p = email_block['block']
#     # Find the closest name block above this email block
#     closest_name = None
#     for nb in reversed(name_blocks):
#         try:
#             if nb['block'].sourceline and email_p.sourceline and nb['block'].sourceline < email_p.sourceline:
#                 closest_name = nb['name']
#                 break
#         except Exception:
#             continue
#     if not closest_name and name_blocks:
#         closest_name = name_blocks[-1]['name']
#     if closest_name and email:
#         professors.append({
#             'Name': closest_name,
#             'Email': email,
#             'University': uni
#         })

with open('professors.json', 'a', encoding='utf-8') as f:
    json.dump(professors, f, ensure_ascii=False, indent=2)

print(f"Extracted {len(professors)} professors from {uni}")
driver.quit()