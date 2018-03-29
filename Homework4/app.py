import os
import requests
import json
from giphy_api_key import api_key
from flask import Flask, render_template, session, redirect, request, url_for, flash
from flask_script import Manager, Shell
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, PasswordField, BooleanField, SelectMultipleField, ValidationError
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from werkzeug.security import generate_password_hash, check_password_hash

# Imports for login management
from flask_login import LoginManager, login_required, logout_user, login_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Application configurations
app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = 'hardtoguessstring'
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL') or "postgresql://postgres:abc123@localhost/mccallauhw4db" 
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# App addition setups
manager = Manager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

# Login configurations setup
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app) # set up login manager

########################
######## Models ########
########################

## Association tables

tags = db.Table('tags',db.Column('term_id',db.Integer, db.ForeignKey('searchterm.id')),db.Column('gif_id',db.Integer, db.ForeignKey('gif.id')))
user_collection = db.Table('user_collection',db.Column('gif_id',db.Integer, db.ForeignKey('gif.id')),db.Column('collection_id',db.Integer, db.ForeignKey('collection.id')))

## User-related Models

# Special model for users to log in
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    usercollection = db.relationship('PersonalGifCollection',backref='User')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

## DB load function
## Necessary for behind the scenes login manager that comes with flask_login capabilities! Won't run without this.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) # returns User object or None

# Model to store gifs
class Gif(db.Model):
	__tablename__ = "gif"
	id = db.Column(db.Integer,primary_key=True)
	title = db.Column(db.String(128))
	embedURL = db.Column(db.String(256))
	def __repr__(self):
		return "(title: {}) (URL: {})".format(self.title, self.embedURL)

# Model to store a personal gif collection
class PersonalGifCollection(db.Model):
	__tablename__ = "collection"
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(255))
	userid = db.Column(db.Integer, db.ForeignKey("users.id"))
	gifs = db.relationship('Gif',secondary=user_collection,backref=db.backref('collection',lazy='dynamic'),lazy='dynamic')

class SearchTerm(db.Model):
	__tablename__ = "searchterm"
	id = db.Column(db.Integer,primary_key=True)
	term = db.Column(db.String(32),unique=True)
	gifs = db.relationship('Gif',secondary=tags,backref=db.backref('searchterm',lazy='dynamic'),lazy='dynamic')
	def __repr__(self):
	    return "(term: {})".format(self.term)

########################
######## Forms #########
########################

# Provided
class RegistrationForm(FlaskForm):
    email = StringField('Email:', validators=[Required(),Length(1,64),Email()])
    username = StringField('Username:',validators=[Required(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'Usernames must have only letters, numbers, dots or underscores')])
    password = PasswordField('Password:',validators=[Required(),EqualTo('password2',message="Passwords must match")])
    password2 = PasswordField("Confirm Password:",validators=[Required()])
    submit = SubmitField('Register User')

    #Additional checking methods for the form
    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already taken')

# Provided
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1,64), Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

# TODO 364: The following forms for searching for gifs and creating collections are provided and should not be edited. You SHOULD examine them so you understand what data they pass along and can investigate as you build your view functions in TODOs below.
class GifSearchForm(FlaskForm):
    search = StringField("Enter a term to search GIFs", validators=[Required()])
    submit = SubmitField('Submit')

class CollectionCreateForm(FlaskForm):
    name = StringField('Collection Name',validators=[Required()])
    gif_picks = SelectMultipleField('GIFs to include')
    submit = SubmitField("Create Collection")

########################
### Helper functions ###
########################

def get_gifs_from_giphy(search_string):
    """ Returns data from Giphy API with up to 5 gifs corresponding to the search input"""
    baseurl = "https://api.giphy.com/v1/gifs/search"
    url = baseurl+'?api_key={}&q={}&limit=5'.format(api_key,search_string)
    resp = json.loads(requests.get(url).text)
    return resp['data']
    
# Provided
def get_gif_by_id(id):
    """Should return gif object or None"""
    g = Gif.query.filter_by(id=id).first()
    return g

def get_or_create_gif(title, url):
	"""Always returns a Gif instance"""
	inst = Gif.query.filter_by(title=title).first()
	if inst:
		return inst
	else:
		gif = Gif(title=title,embedURL=url)
		db.session.add(gif)
		db.session.commit()
		return gif

def get_or_create_search_term(term):
	"""Always returns a SearchTerm instance"""
	inst = SearchTerm.query.filter_by(term=term).first()
	if not inst:
		inst = SearchTerm(term=term)
	data = get_gifs_from_giphy(term)
	for gif in data:
		title = gif['title']
		url = gif['embed_url']
		gif = get_or_create_gif(title,url)
		inst.gifs.append(gif)
	db.session.add(inst)
	db.session.commit()
	return inst

def get_or_create_collection(name, current_user, gif_list=[]):
    """Always returns a PersonalGifCollection instance"""
    inst = PersonalGifCollection.query.filter_by(name=name,userid=current_user.id).first()
    if not inst:
    	inst = PersonalGifCollection(name=name,userid=current_user.id)
    	for gif in gif_list:
    		inst.gifs.append(gif)
    	db.session.add(inst)
    	db.session.commit()
    return inst


########################
#### View functions ####
########################

## Error handling routes
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


## Login-related routes - provided
@app.route('/login',methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('index'))
        flash('Invalid username or password.')
    return render_template('login.html',form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('index'))

@app.route('/register',methods=["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,username=form.username.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You can now log in!')
        return redirect(url_for('login'))
    if form.errors: flash([error for errors in form.errors.values() for error in errors])
    return render_template('register.html',form=form)

@app.route('/secret')
@login_required
def secret():
    return "Only authenticated users can do this! Try to log in or contact the site admin."

## Other routes
@app.route('/', methods=['GET', 'POST'])
def index():
    form = GifSearchForm()
    if form.validate_on_submit():
    	term = form.search.data
    	func = get_or_create_search_term(term)
    	return redirect(url_for('search_results',search_term=term))
    if form.errors: flash([error for errors in form.errors.values() for error in errors])
    return render_template('index.html',form=form)

# Provided
@app.route('/gifs_searched/<search_term>')
def search_results(search_term):
    term = SearchTerm.query.filter_by(term=search_term).first()
    relevant_gifs = term.gifs.all()
    return render_template('searched_gifs.html',gifs=relevant_gifs,term=term)

@app.route('/search_terms')
def search_terms():
	all_terms = SearchTerm.query.all()
	return render_template('search_terms.html',all_terms=all_terms)

# Provided
@app.route('/all_gifs')
def all_gifs():
    gifs = Gif.query.all()
    return render_template('all_gifs.html',all_gifs=gifs)

@app.route('/create_collection',methods=["GET","POST"])
@login_required
def create_collection():
    form = CollectionCreateForm()
    gifs = Gif.query.all()
    choices = [(str(g.id), g.title) for g in gifs]
    form.gif_picks.choices = choices
    if form.validate_on_submit():
    	gifs = [get_gif_by_id(int(pick)) for pick in form.gif_picks.data]
    	collection = get_or_create_collection(form.name.data,current_user,gifs)
    	return redirect(url_for('collections'))
    if form.errors: flash([error for errors in form.errors.values() for error in errors])
    return render_template('create_collection.html',form=form)

@app.route('/collections',methods=["GET","POST"])
@login_required
def collections():
	collections = PersonalGifCollection.query.filter_by(userid=current_user.id)
	return render_template('collections.html',collections=collections)

# Provided
@app.route('/collection/<id_num>')
def single_collection(id_num):
    id_num = int(id_num)
    collection = PersonalGifCollection.query.filter_by(id=id_num).first()
    gifs = collection.gifs.all()
    return render_template('collection.html',collection=collection, gifs=gifs)

if __name__ == '__main__':
    db.create_all()
    manager.run()
