

from flask import Flask
import feedparser
import json
import urllib.parse
import urllib.request
from flask import render_template
from flask import request



app = Flask(__name__)
DEFAULTS = {
    'publication':'bbc',
    'city':'Lagos'
}
RSS_FEED ={'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
           'cnn':'http://rss.cnn.com/rss/edition.rss',
           'fox':'http://feeds.foxnews.com/foxnews/latest',
           'iol':'http://www.iol.co.za/cmlink/1.640'}



@app.route("/")
def home():
    publication = request.args.get("publication")
    if not publication:
        publication = DEFAULTS["publication"]
    articles = get_news(publication)
    city = request.args.get("city")
    if not city:
        city = DEFAULTS['city']
    weather = get_weather(city)
    return render_template("home.html",articles=articles,weather=weather)
def get_news(query):
    if not query or query.lower() not in RSS_FEED:
        publication = DEFAULTS["publication"]
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEED[publication])

    return feed["entries"]
def get_weather(query):
    api_url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid=907ca5c7ebf96a13e435f2ce904ecef3"
    query = urllib.parse.quote(query)
    url = api_url.format(query)
    data = urllib.request.urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather = {
            "description" : parsed["weather"][0]["description"],
            "temperature": parsed["main"]["temp"],
            "city":parsed['name']
        }
    return weather
if __name__ == "__main__":
    app.run()