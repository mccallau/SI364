# __authors__ = Julia Locke, Jackie Cohen

import json
import requests
import os
from flask import Flask, request, render_template, session, redirect, url_for, flash
from flask import jsonify
from flask_script import Manager, Shell
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, PasswordField, BooleanField, ValidationError, SelectMultipleField
from wtforms.validators import Required, Email, EqualTo
from flask_sqlalchemy import SQLAlchemy
import random
from flask_migrate import Migrate, MigrateCommand

api_key = '676ee8b4f0e9d24b7782f1915262b042'
# Get your own API key from: https://developers.zomato.com/api (Scroll to Generate an API key)
# Of course, you can also check out the code and try it otherwise, iteratively (bit by bit)

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = 'random string'
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:abc123@localhost/lecture12example"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



manager = Manager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


cuisine_restaurant = db.Table('cuisine_restaurant',db.Column('restuarant_id',db.Integer, db.ForeignKey('restaurants.id')),db.Column('cuisine_id',db.Integer,db.ForeignKey('cuisines.id')))

class Restaurant(db.Model):
	__tablename__ = "restaurants"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64))
	city_id = db.Column(db.Integer, db.ForeignKey("cities.id"))
	cuisines = db.relationship('Cuisine', secondary=cuisine_restaurant,backref=db.backref('restaurants',lazy='dynamic'),lazy='dynamic')

class City(db.Model):
	__tablename__ = "cities"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64))

class Cuisine(db.Model):
	__tablename__ = "cuisines"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64))


def get_city_code(city):
	try:
		headers = {'user-key':api_key}
		params = {'q':city}
		response = requests.get('https://developers.zomato.com/api/v2.1/cities', headers=headers, params=params)
		data = json.loads(response.text)
		for each in data['location_suggestions']:
			if each['name'].upper() == city.upper():
				return each['id']
	except:
		return None

def get_cuisine_code(cuisine, city_code):
	try:
		headers = {'user-key':api_key}
		params = {'city_id':city_code}
		response = requests.get('https://developers.zomato.com/api/v2.1/cuisines', headers=headers, params=params)
		data = json.loads(response.text)
		for each in data['cuisines']:
			if each['cuisine']['cuisine_name'].upper() == cuisine.upper():
				return str(each['cuisine']['cuisine_id'])
	except:
		return None

def get_restaurants(cuisine, city):
	try:
		city_code = get_city_code(city)
		cuisine_code = get_cuisine_code(cuisine, city_code)
		headers = {'user-key':api_key}
		params = {'user-key':api_key, 'entity_id':city_code, 'entity_type':'city', 'cuisines':cuisine_code,'count':50}
		response = requests.get('https://developers.zomato.com/api/v2.1/search', headers=headers, params=params)
		data = json.loads(response.text)
		return data['restaurants']
	except:
		return 'Trouble finding restaurant data'

class RestaurantForm(FlaskForm):
	cuisine = StringField('What kind of food are you in the mood for?')
	city = StringField('What city do you want to search in?')
	submit = SubmitField('Search')

def get_or_create_city(db_session, city):
	new_city = db_session.query(City).filter_by(name=city).first()
	if new_city:
		return new_city
	else:
		new_city = City(name=city)
		db_session.add(new_city)
		db_session.commit()
		return new_city

def get_or_create_cuisine(db_session, cuisine):
	new_cuisine = db_session.query(Cuisine).filter_by(name=cuisine).first()
	if new_cuisine:
		return new_cuisine
	else:
		new_cuisine = Cuisine(name=cuisine)
		db_session.add(new_cuisine)
		db_session.commit()
		return new_cuisine

def get_or_create_restaurant(db_session, restaurant_name, city_name, cuisines_list = []):
	city = get_or_create_city(db_session, city=city_name)
	restaurant = db_session.query(Restaurant).filter_by(name=restaurant_name, city_id=city.id).first()
	if restaurant:
		return restaurant
	else:
		restaurant = Restaurant(name=restaurant_name, city_id=city.id)
		for cuisine in cuisines_list:
			cuisine = get_or_create_cuisine(db_session, cuisine=cuisine)
			restaurant.cuisines.append(cuisine)
		db_session.add(restaurant)
		db_session.commit()
		return restaurant

@app.errorhandler(404)
def page_not_found(e):
	return render_template('error404.html'), 404

@app.errorhandler(500)
def internal_server_error():
	return render_template('error505.html'), 500

@app.route('/', methods=["GET", "POST"])
def welcomepage():
	form = RestaurantForm()
	if form.validate_on_submit():
		cuisine = form.cuisine.data
		city = form.city.data
		session['cuisine'] = cuisine
		session['city'] = city
		restaurant_data = get_restaurants(cuisine=cuisine, city=city)
		return render_template('addrestaurants.html', data=restaurant_data)
	return render_template('welcomepage.html', form=form)

@app.route('/ajax')
def great_search():
    x = jsonify({"livingston" : [{'name' : restaurant['restaurant']['name']} for restaurant in get_restaurants("American", "Detroit, MI")]})
    return x

@app.route('/ajax2')
def great_search2():
    x = jsonify({'austin':[{'classes':"Si 364"},{'classes':"Si 340"},{'classes':"Si 330"}]})
    return x

if __name__ == '__main__':
    db.create_all()
    manager.run()
