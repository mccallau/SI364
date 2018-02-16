from flask import Flask, request, render_template, url_for, flash, redirect
from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, ValidationError, StringField
from wtforms.validators import Required, Length
import json
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard2oguessstring'

def zipvalidator(form, field):
		if len(field.data)==5:
			try:
				json.loads(requests.get('http://api.openweathermap.org/data/2.5/weather?APPID=71460048a19286069e143a61cdc3a5b5&zip='+field.data+',us').text)['name'] 
			except:
				raise ValidationError("Invalid zip code: zip code does not exist")
		else:
			raise ValidationError("Invalid zip code: zip code must be 5 digits")

class weatherform(FlaskForm):
	weather = StringField('Enter a 5-digit zipcode: ',validators=[zipvalidator])
	submit = SubmitField('Submit')

@app.route('/zipcode',methods=['POST','GET'])
def zipcode():
	form=weatherform()
	if request.method=='POST' and form.validate_on_submit():
		form=weatherform(request.form)
		call=requests.get('http://api.openweathermap.org/data/2.5/weather?APPID=71460048a19286069e143a61cdc3a5b5&zip='+form.weather.data+',us')
		call=json.loads(call.text)
		name=call['name']
		weather=call['weather'][0]['description']
		temp=str(int(call['main']['temp'])-273)+' celsius'
		return render_template('zipcode.html',form=form,name=name,weather=weather,temp=temp,error="")
	flash(form.errors)
	return render_template('zipcode.html',form=form,name='',weather='',temp='',error='')

if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)
