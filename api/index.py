from flask import Flask, jsonify, request
from flask_cors import cross_origin
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    return 'Working Fine AF. Try with "/scrape?limit=10" Endpoint'

@app.route('/scrape')
@cross_origin()
def scrape():
    url = 'https://finshots.in/archive/'
    articles = []
    count = 0
    limit = int(request.args.get('limit', 24))
    while url:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for post_card in soup.find("div", class_="post-feed").find_all("article", class_="post-card"):
            title = post_card.find("h2", class_="post-card-title").get_text()
            date = post_card.find("footer", class_="post-card-meta").find("time", class_="post-full-meta-date").get_text()
            excerpt = post_card.find("section", class_="post-card-excerpt").find("p").get_text()
            img_src = post_card.find("a", class_="post-card-image-link").find("img", class_="post-card-image")['src']
            link = 'https://finshots.in' + post_card.find("a", class_="post-card-image-link")['href']
            sname = "Finshots"
            articles.append({'title': title, 'createdAt': date, 'content': excerpt, 'imageUrl': img_src, 'sourceUrl': link, 'sourceName': sname})
            count += 1
        if count < int(request.args.get('limit', 24)):
            # find the next button to navigate to the next page
            next_button = soup.find("a", class_="older-posts")
            if next_button:
                url = 'https://finshots.in' + next_button['href']
            else:
                url = None
        else:
            url = None
    count = min(count, limit)
    data = {"data": {"count": count, "articles": articles[:limit]}}
    return jsonify(data)

if __name__ == '__main__':
    app.run()
