

from flask import Flask,render_template,request
import feedparser
import json
import urllib.parse
import urllib.request




app = Flask(__name__)
DEFAULTS = {
    'publication':'bbc',
    'city':'Lagos'
}
RSS_FEED ={'bbc': 'https://feeds.bbci.co.uk/news/rss.xml',
           'cnn':'https://rss.cnn.com/rss/edition.rss',
           'fox':'https://feeds.foxnews.com/foxnews/latest',
           'iol':'https://www.iol.co.za/cmlink/1.640'}

API_KEY= "907ca5c7ebf96a13e435f2ce904ecef3"


@app.route("/")
def home():
    publication = request.args.get("publication")
    if not publication:
        publication = DEFAULTS["publication"]
    articles = get_news(publication)
    city = request.args.get("city")
    if not city:
        city = DEFAULTS['city']
    city =city.strip()
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
    query = urllib.parse.quote(query)
    api_url = f"https://api.openweathermap.org/data/2.5/weather?q={query}&units=metric&appid={API_KEY}"


    data = urllib.request.urlopen(api_url).read()
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
    app.run(debug=True)