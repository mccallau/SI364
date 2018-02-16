# Import statements
import os
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import Required, Length
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, Shell # New

# Basic Flask application setup
basedir = os.path.abspath(os.path.dirname(__file__)) # In case we need to reference the base directory of the application
# To set up application and defaults for running
app = Flask(__name__)
app.debug = True
app.use_reloader = True

app.config['SECRET_KEY'] = 'hardtoguessstring'
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:abc123@localhost/shelldb_example" # TODO: May need to change this, Windows users. Everyone will need to have created a db with exactly this name.
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

## Setup
manager = Manager(app) # In order to use manager
db = SQLAlchemy(app) # For database use

## Models
class Movie(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64))
    year = db.Column(db.String(10))

class Director(db.Model):
    __tablename__ = "directors"
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255))
    city = db.Column(db.String(64))

## Forms
class MovieForm(FlaskForm):
    name = StringField("Enter the name of a movie you like:", validators=[Required(),Length(1,64)])
    year = StringField("Enter the year it was released (YYYY):",validators=[Required(),Length(4,5)])
    submit = SubmitField()

class DirectorForm(FlaskForm):
    person_name = StringField("Enter the name of a director you like:",validators=[Required()])
    city = StringField("Enter the city that person lives in:",validators=[Required()])
    submit = SubmitField()

## Routes & view functions
@app.route('/',methods=["GET","POST"])
def home():
    form1 = MovieForm()
    form2 = DirectorForm()

    moviename,movieyr,directorname,dir_city = None,None,None,None
    if form1.validate_on_submit():
        moviename = form1.name.data
        movieyr = form1.year.data
        movie = Movie(name=moviename,year=movieyr)
        db.session.add(movie)
        db.session.commit()
        return redirect(url_for('get_movies'))

    if form2.validate_on_submit():
        directorname = form2.person_name.data
        dir_city = form2.city.data
        director = Director(full_name=directorname,city=dir_city)
        db.session.add(director)
        db.session.commit()
        return redirect(url_for('get_directors'))

    return render_template('home.html',form1=form1, form2=form2)

@app.route('/movies')
def get_movies():
    movies = Movie.query.all()
    return render_template('movies.html',movies=movies)

@app.route('/directors')
def get_directors():
    dirs = Director.query.all()
    return render_template("directors.html",directors=dirs)

if __name__ == "__main__":
    db.create_all()
    manager.run()
