
import os
from flask import Flask,render_template,request,make_response
import feedparser
import requests
import datetime
import urllib.parse
import urllib.request


app = Flask(__name__)
DEFAULTS = {
    'publication':'bbc',
    'city':'Lagos',
    "currency_from":"NGN",
    "currency_to":"USD"
}
RSS_FEED ={'bbc': 'https://feeds.bbci.co.uk/news/rss.xml',
           'cnn':'https://rss.cnn.com/rss/edition.rss',
           'fox':'https://feeds.foxnews.com/foxnews/latest',
           'iol':'https://www.iol.co.za/cmlink/1.640'}

API_KEY= os.getenv("WEATHER_API_KEY")
CurrencyApi = os.getenv("CURRENCY_API")

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
    currency_from = request.args.get("currency_from")
    if not currency_from:
        currency_from =DEFAULTS["currency_from"]
    currency_to = request.args.get("currency_to")
    if not currency_to:
        currency_to = DEFAULTS["currency_to"]
    rate,currencies = get_rates(currency_from,currency_to)

    return render_template("home.html",
                           articles=articles,
                           weather=weather,
                           currency_to=currency_to,
                           currency_from=currency_from,
                           rate=rate,currencies=sorted(currencies))

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
    data = requests.get(api_url)
    parsed = data.json()
    weather = None
    if parsed.get("weather"):
        weather = {
            "description" : parsed["weather"][0]["description"],
            "temperature": parsed["main"]["temp"],
            "city":parsed['name']
        }
    return weather
def get_rates(frm,to):
    currency_url = f"https://openexchangerates.org/api/latest.json?app_id={CurrencyApi}"
    all_currency = requests.get(currency_url)
    data = all_currency.json()
    rates = data.get("rates",{})
    frm_rates = rates.get(frm.upper())
    to_rates = rates.get(to.upper())

    if frm_rates and to_rates:
        return to_rates/frm_rates,rates.keys()
    return None

if __name__ == "__main__":
    app.run(debug=True)