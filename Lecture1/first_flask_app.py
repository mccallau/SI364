# Import statements necessary
from flask import Flask, render_template
import requests
import json

# Set up application
app = Flask(__name__)

# Routes

@app.route('/')
def another_function():
    return 'Hello World!'

@app.route('/user/<yourname>')
def hello_name(yourname):
    return '<h1>Hello {}</h1>'.format(yourname)

# new route: /itunes/<artist>
@app.route('/itunes/<artist>')
def artist_hi(artist):
	artist = artist.replace(" ","+")
	rq = requests.get('https://itunes.apple.com/search?term='+artist+'&entity=song&attribute=allArtistTerm')
	ls = []
	rq = json.loads(rq.text)
	for x in rq['results']:
		ls.append(x['trackName'])
	return '<h1>{}</h1>'.format(str(ls))

if __name__ == '__main__':
    app.run()

