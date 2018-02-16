# Import statements
import os
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, ValidationError
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
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:Mudkipper16!@localhost/weatherdb" # TODO: May need to change this, Windows users. Everyone will need to have created a db with exactly this name.
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

## Setup
manager = Manager(app) # In order to use manager
db = SQLAlchemy(app) # For database use

## Models
class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    temp_fah = db.Column(db.Integer)

## Forms
class CityForm(FlaskForm):
    name = StringField("Enter the name of a city:",validators=[Required()])
    temp = IntegerField("Enter the temperature in Fahrenheit degrees:",validators=[Required()])
    submit = SubmitField()

## Helper functions (if any)

## Routes
@app.route('/')
def index():
    num_cities = len(Weather.query.all())
    return render_template('home.html',num_cities=num_cities)

@app.route('/form', methods=["GET","POST"])
def enter_info():
    form = CityForm()
    if form.validate_on_submit():
        name = form.name.data
        temp = form.temp.data
        citytemp = Weather(name=name,temp_fah=temp)
        db.session.add(citytemp)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('formshow.html',form=form)

@app.route('/cities_and_temps')
def cities_and_temps():
    cities = Weather.query.all()
    return render_template('cities.html',cities=cities)

if __name__ == "__main__":
    db.create_all()
    manager.run()
