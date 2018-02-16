from flask import Flask, render_template, request
import json
import requests

app = Flask(__name__)

# Challenge 1: Return the 404.html template
# Edit it such that it displays an interesting message

# Challenge 2: Include the link to homepage i.e. http://localhost:5000 in 404.html.
## YOUR CODE HERE

# Challenge 3: Write an error handler for 500 error
## YOUR CODE HERE

# Challenge 4: Edit the 500.html template to display link to homepage and link to itunes-form.


@app.route('/')
def index():
    return "Hello, World!"

@app.route('/itunes-form')
def ituneForm():
	return render_template('itunes-form.html')

@app.route('/itunes-result',methods=['GET'])
def resultTunes():
	name=request.args.get('artist')
	num=request.args.get('num')
	result=json.loads(requests.get('https://itunes.apple.com/search?term={}&media=music&entity=song'.format(name)).text)['results'][:int(num)]
	result=[x['trackName'] for x in result]
	return render_template('itunes-result.html',name=name,num=num,result=result)

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html')

@app.errorhandler(500)
def page_failure(e):
	return render_template('500.html')

if __name__ == '__main__':
    app.run(debug = True)
