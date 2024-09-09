import requests
from bs4 import BeautifulSoup
import json

def scrape_news_article(url):
    # Send a GET request to the website
    response = requests.get(url)
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the <script> tag with type="application/ld+json"
    script_tag = soup.find('script', type='application/ld+json')
    
    # Check if the <script> tag exists
    if script_tag:
        try:
            # Load the JSON content from the <script> tag
            json_data = json.loads(script_tag.string)
            
            # Print the raw JSON data for inspection
            print("Raw JSON Data:")
            print(json.dumps(json_data, indent=4))  # Pretty print the JSON data
            
            # Check if the JSON data is a list and contains at least one dictionary
            if isinstance(json_data, list) and len(json_data) > 0:
                article = json_data[0]
                
                # Extract the relevant fields from the article data
                title = article.get('headline', '')
                description = article.get('description', '')
                link = article.get('url', '')
                img_url = article.get('image', [''])[0]
                articleBody = article.get('articleBody', '')
                author = article.get('author', {}).get('name', '')
                publisher_name = article.get('publisher', {}).get('name', '')
                publisher_logo = article.get('publisher', {}).get('logo', {}).get('url', '')
                
                # Print or return the extracted details
                print(f"Title: {title}")
                print(f"Description: {description}")
                print(f"Link: {link}")
                print(f"Image URL: {img_url}")
                print(f"Author: {author}")
                print(f"Publisher Name: {publisher_name}")
                print(f"Publisher Logo: {publisher_logo}")
            else:
                print("JSON data is not in expected format.")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
    else:
        print("No JSON-LD script tag found.")

# Example usage
scrape_news_article('https://www.moneycontrol.com/news/india/change-of-heart-why-aap-and-congress-are-ready-to-bet-on-each-other-in-haryana-12813579.html')
