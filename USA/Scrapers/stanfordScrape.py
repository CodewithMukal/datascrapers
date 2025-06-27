import json
import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin, urlparse
import re

# CLAUDE WROTE THIS ONE ITS TOO LONG!!

with open('links.json','r') as f:
    links = json.load(f)
    "key is the name of uni and value is link, i want to make an array of links"
    uni_links = list(links["USA"].values())


def scrape_professor_emails(base_url):
    """
    Scrape professor emails from university AI department page
    """
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    
    professors_data = []
    
    try:
        print(f"🔍 Fetching main page: {base_url}")
        response = session.get(base_url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        print("✅ Successfully fetched main page")
        
        # Find div with class "clearfix"
        clearfix_div = soup.find('div', class_='clearfix')
        if not clearfix_div:
            print("❌ No div with class 'clearfix' found")
            return professors_data
        
        print("✅ Found div with class 'clearfix'")
        
        # Get child divs
        child_divs = clearfix_div.find_all('div', recursive=False)
        print(f"📊 Found {len(child_divs)} direct child divs")
        
        if len(child_divs) < 2:
            print("❌ Less than 2 child divs found")
            return professors_data
        
        # Check second child div for h2 with "Artificial Intelligence"
        second_div = child_divs[1]
        print("🔍 Checking second child div...")
        
        ai_h2 = second_div.find('h2')
        if not ai_h2:
            print("❌ No h2 tag found in second child div")
            return professors_data
        
        h2_text = ai_h2.get_text(strip=True)
        print(f"📝 Found h2 text: '{h2_text}'")
        
        if "Artificial Intelligence" not in h2_text:
            print("❌ H2 does not contain 'Artificial Intelligence'")
            return professors_data
        
        print("✅ Confirmed h2 contains 'Artificial Intelligence'")
        
        # Find ul within the second div
        ul_element = second_div.find('ul')
        if not ul_element:
            print("❌ No ul element found in second div")
            return professors_data
        
        print("✅ Found ul element")
        
        # Iterate through list items
        list_items = ul_element.find_all('li')
        print(f"📊 Found {len(list_items)} list items")
        
        for i, li in enumerate(list_items, 1):
            print(f"\n🔍 Processing list item {i}/{len(list_items)}")
            
            # Find article element deep in the chain
            article = li.find('article')
            if not article:
                print(f"⚠️  No article element found in list item {i}")
                continue
            
            print(f"✅ Found article element in list item {i}")
            
            # Find div with class "su-card__contents"
            card_contents = article.find('div', class_='su-card__contents')
            if not card_contents:
                print(f"⚠️  No div with class 'su-card__contents' found in list item {i}")
                continue
            
            print(f"✅ Found su-card__contents div in list item {i}")
            
            # Find h3 with anchor tag
            h3_element = card_contents.find('h3')
            if not h3_element:
                print(f"⚠️  No h3 element found in list item {i}")
                continue
            
            anchor = h3_element.find('a')
            if not anchor:
                print(f"⚠️  No anchor tag found in h3 of list item {i}")
                continue
            
            # Extract professor name and link
            prof_name = anchor.get_text(strip=True)
            prof_link = anchor.get('href')
            
            if not prof_link:
                print(f"⚠️  No href found in anchor of list item {i}")
                continue
            
            # Convert relative URL to absolute
            prof_url = urljoin(base_url, prof_link)
            
            print(f"👨‍🏫 Professor found: {prof_name}")
            print(f"🔗 Professor URL: {prof_url}")
            
            # Scrape professor's email
            email = scrape_professor_email(session, prof_url, prof_name)
            
            professors_data.append({
                'name': prof_name,
                'url': prof_url,
                'email': email
            })
            
            # Be respectful to the server
            time.sleep(1)
    
    except requests.RequestException as e:
        print(f"❌ Request error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    return professors_data

def scrape_professor_email(session, prof_url, prof_name):
    """
    Scrape email from professor's individual page
    """
    try:
        print(f"📧 Fetching email for {prof_name}...")
        response = session.get(prof_url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find anchor tag with class "mail"
        mail_anchor = soup.find('a', class_='mail')
        
        if mail_anchor:
            email_text = mail_anchor.get_text(strip=True)
            # Also check href attribute for mailto links
            href = mail_anchor.get('href', '')
            
            # Extract email from mailto: links
            if href.startswith('mailto:'):
                email = href.replace('mailto:', '').split('?')[0]
            else:
                email = email_text
            
            # Validate email format
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            if re.match(email_pattern, email):
                print(f"✅ Email found for {prof_name}: {email}")
                return email
            else:
                print(f"⚠️  Invalid email format found for {prof_name}: {email}")
        
        # Fallback: search for any email pattern on the page
        page_text = soup.get_text()
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, page_text)
        
        if emails:
            email = emails[0]  # Take the first email found
            print(f"✅ Email found via pattern search for {prof_name}: {email}")
            return email
        else:
            print(f"❌ No email found for {prof_name}")
            return None
            
    except requests.RequestException as e:
        print(f"❌ Request error for {prof_name}: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error for {prof_name}: {e}")
        return None

# Main execution
if __name__ == "__main__":
    if len(uni_links) < 2:
        print("❌ uni_links[1] is not available")
        exit(1)
    
    base_url = uni_links[1]
    
    if not base_url:
        print("❌ uni_links[1] is empty")
        exit(1)
    
    print("🚀 Starting AI Professors Email Scraping")
    print("=" * 50)
    
    professors = scrape_professor_emails(base_url)
    
    print("\n" + "=" * 50)
    print("📊 SCRAPING RESULTS")
    print("=" * 50)
    
    if professors:
        print(f"✅ Successfully scraped {len(professors)} professors")
        for i, prof in enumerate(professors, 1):
            print(f"\n{i}. Name: {prof['name']}")
            print(f"   URL: {prof['url']}")
            print(f"   Email: {prof['email'] if prof['email'] else 'Not found'}")
    else:
        print("❌ No professors found or scraping failed")
    

    for prof in professors:
        if(prof["email"]!="Not found"):
            with open('professors.json', 'a') as f:
                # I want to write the data as "Name": prof['name], "Email": prof['email'], "University": "Stanford University"
                f.write(f'{{"Name": "{prof["name"]}", "Email": "{prof["email"]}", "University": "Stanford University"}}\n')
        else:
                f.write('\n')
    print("\n🏁 Scraping completed!")