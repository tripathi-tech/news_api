from flask import Flask, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": ["http://localhost:3000", "https://news-1u4o0wxg4-tripathitechs-projects.vercel.app"]}})

def scrape_news():
    response = requests.get('https://www.moneycontrol.com/news/india/')
    soup = BeautifulSoup(response.text, 'html.parser')
    li_elements = soup.find_all('li', attrs={'class': 'clearfix'})
    articles = []
    
    for li in li_elements:
        anchor = li.find('a')
        img_tag = li.find('img')
        title = img_tag['title'] if img_tag else ''
        link = anchor['href'] if anchor else ''
        description = li.find('p').get_text(strip=True) if li.find('p') else ''
        img_url = img_tag['data-src'] if img_tag else ''

        articles.append({
            'title': title,
            'link': link,
            'description': description,
            'img_url': img_url
        })
    
    return articles

@app.route('/news', methods=['GET'])
def get_news():
    articles = scrape_news()
    return jsonify(articles)

if __name__ == '__main__':
    app.run(debug=True)
