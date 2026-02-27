from flask import Flask
import feedparser
from flask import render_template

app = Flask(__name__)
RSS_FEED ={'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
           'cnn':'http://rss.cnn.com/rss/edition.rss',
           'fox':'http://feeds.foxnews.com/foxnews/latest',
           'iol':'http://www.iol.co.za/cmlink/i.640'}



def get_news(publication):
    feed = feedparser.parse(RSS_FEED[publication])
    return render_template("home.html",
                           articles = feed['entries'])

@app.route("/")
@app.route("/bbc")
def bbc():
    return get_news("bbc")
@app.route("/cnn")
def cnn():
    return get_news("cnn")
if __name__ == "__main__":
    app.run()