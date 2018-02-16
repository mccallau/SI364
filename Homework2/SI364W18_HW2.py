## SI 364
## Winter 2018
## HW 2 - Part 1

## This homework has 3 parts, all of which should be completed inside this file (and a little bit inside the /templates directory).

## Add view functions and any other necessary code to this Flask application code below so that the routes described in the README exist and render the templates they are supposed to (all templates provided are inside the templates/ directory, where they should stay).

## As part of the homework, you may also need to add templates (new .html files) to the templates directory.

#############################
##### IMPORT STATEMENTS #####
#############################
from flask import Flask, request, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError
from wtforms.validators import Required
import json
import requests

#####################
##### APP SETUP #####
#####################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'

####################
###### FORMS #######
####################




####################
###### ROUTES ######
####################

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/user/<name>')
def hello_user(name):
    return '<h1>Hello {0}<h1>'.format(name)


@app.route('/artistform')
def artistform():
	return render_template('artistform.html')


@app.route('/artistinfo',methods=['GET'])
def artistinfo():
	form=request.args.get('artist')
	rq = requests.get('https://itunes.apple.com/search?term='+form+'&media=music&attribute=artistTerm')
	ob=json.loads(rq.text)['results']
	return render_template('artist_info.html',objects=ob)


@app.route('/artistlinks')
def artistlinks():
	return render_template('artist_links.html')


@app.route('/specific/song/<artist_name>')
def specificsong(artist_name):
	rq = requests.get('https://itunes.apple.com/search?term='+artist_name+'&media=music&attribute=artistTerm')
	ob=json.loads(rq.text)['results']
	return render_template('specific_artist.html',results=ob)


class AlbumEntryForm(FlaskForm):
	name = StringField('Enter the name of an album:', validators=[Required()])
	likes = RadioField('How much do you like this album? (1 low, 3 high)', choices=[(1,'1'),(2,'2'),(3,'3')],validators=[Required()])
	submit = SubmitField('Submit')

@app.route('/album_entry')
def albumentry():
	form=AlbumEntryForm()
	return render_template('album_entry.html',form=form)


@app.route('/album_result',methods=['GET'])
def albumresult():
	name=request.args.get('name')
	likes=request.args.get('likes')
	rq = requests.get('https://itunes.apple.com/search?term='+name+'&media=music&attribute=albumTerm&entity=album')
	ob=json.loads(rq.text)['results']
	return render_template('album_data.html',name=name,likes=likes,results=ob)

if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)
