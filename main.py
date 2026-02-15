from flask import Flask
import feedparser

BBC_FEED = "https://feeds.bbci.co.uk/news/rss.xml"
app = Flask(__name__)
@app.route("/")
def get_news():
    feed = feedparser.parse(BBC_FEED)
    firstArticle = feed["entries"][0]

    return '''<html>
    <body>
        <h1> BBC Headlines </h1>
        <b>{0}</b> <br/>
        <i>{1}</i> <br/>
        <p> {2}</p> <br/>
    </body>
     </html>'''.format(firstArticle.get("title"),firstArticle.get("published"),firstArticle.get("summary"))
if __name__ == "__main__":
    app.run()
