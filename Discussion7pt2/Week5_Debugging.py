##Debug this code to get articles from Buzzfeed
from flask import Flask, request, render_template
import json
app = Flask(__name__)
app.debug = True

@app.route('/')
def hello_to_you():
    return 'Hello!'

class buzzForm():
    pass

@app.route("/buzzfeed")
def buzzfeed():
    form = buzzForm()
    render_template('buzzfeed.html')


@app.route("/buzzfeed_articles")
def buzzfeed_articles():
    response_dict = {}
    final_response_dict = {}
    baseurl = "https://www.buzzfeed.com/api/v2/feeds/"


    render_template('article_links.html')

if __name__ == '__main__':
    app.run()