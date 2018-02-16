from flask import Flask, request, render_template, flash, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, DateField, IntegerField, BooleanField, ValidationError # see some new ones... + ValidationError
from wtforms.validators import Required, Length, Email, Regexp

#####################
##### APP SETUP #####
#####################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string' # Can be whatever for us, for now; this is what 'seeds' the CSRF protection
app.debug=True

####################
###### FORMS #######
####################

class SecretClubForm(FlaskForm):
    name = StringField("Enter the name of your secret club:", validators=[Required(),Length(3,64)]) # Must be at least 3 and no more than 64 chars
    number_members = StringField("How many people may be in this secret club (must enter an integer):", validators=[Required(),Regexp('^\d+$')]) # Validated with a regular expression: only digits
    passcode = StringField("What is the secret code to enter the secret society? Must not have any vowels.",validators=[Required()]) # Required, plus the below validator...
    submit = SubmitField("Submit")
    def validate_passcode(form, field):
        vowels='aeiou'
        ## With code here -- I had 2 lines above the code already provided to make it so that this validator would reject anything with vowels. Could also do it in 1 line.
        for ch in str(form.passcode.data): # REPLACE THIS LINE WITH SOMETHING ELSE
            if ch in vowels:
                raise ValidationError("Your passcode was not valid because there was at least 1 vowel in it."+str(form.passcode.data))

####################
###### ROUTES ######
####################

@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/form')
def form_entry():
    form = SecretClubForm()
    return render_template('form.html',form=form)


@app.route('/answers',methods=['POST'])
def show_answers():
    form = SecretClubForm(request.form)
    if form.validate_on_submit():
        name = form.name.data
        passcode = form.passcode.data
        capacity = form.number_members.data
        return render_template('results.html',name=name,passcode=passcode,capacity=capacity)
    flash(form.errors)
    return redirect(url_for('form_entry'))

if __name__ == "__main__":
    app.run(use_reloader=True,debug=True)
