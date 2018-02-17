###############################
####### SETUP (OVERALL) #######
###############################

# Import statements
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, ValidationError
from wtforms.validators import Required, Length
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, Shell
import json

# App setup code
app = Flask(__name__)
app.debug = True
app.use_reloader = True

# All app.config values
app.config['SECRET_KEY'] = 'hard to guess string'
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:abc123@localhost/bookauthordb" # TODO: May need to change this, Windows users -- probably by adding postgres:YOURTEXTPW@localhost instead of just localhost. Or just like you did in section or lecture before! Everyone will need to have created a db with exactly this name, though.
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Other setup
manager = Manager(app) # In order to use manager
db = SQLAlchemy(app) # For database use

#############################
######## HELPER FXNS ########
#############################

# (More challenging) Define a function called get_or_create_author.
# It should accept an author name and return a Author object (an instance of model Author).
# It should check whether there exists a author by the input name. If there is, it should return that author. If there is not, it should create and save to the database a author with that name, and return the new Author instance.


# (Easier) Define a function called get_book_info that takes as input a string representing a book title, searches for that title with a request to the iTunes API for media type "ebook" (check out the documentation!), and returns a Python object representation of the data resulting from that API request.

def get_book_info(title):
    url='https://itunes.apple.com/search?entity=ebook&term='+title
    return json.loads(requests.get(url).text)

def get_or_create_author(name):
    author =  Author.query.filter_by(name=name).first()
    if not author:
        author=Author(name=name)
        db.session.add(author)
        db.session.commit()
    return author

##################
##### MODELS #####
##################

class Author(db.Model):
    __tablename__ = "authors"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(255))
    books = db.relationship('Book',backref='Author')

class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(255))
    author_id = db.Column(db.Integer,db.ForeignKey("authors.id"))


###################
###### FORMS ######
###################

class EnterBookAuthor(FlaskForm):
    title = StringField("Enter the title of a book.",validators=[Required()])
    author = StringField("Enter the author's name.",validators=[Required()])
    submit = SubmitField()

#######################
###### VIEW FXNS ######
#######################

# Note: In THIS application, you can't enter duplicate authors (if you enter the same author again, it doesn't save a NEW author), but you COULD enter duplicate books.
@app.route('/',methods=['GET','POST'])
def home():
    form = EnterBookAuthor()
    if form.validate_on_submit():
        booktitle = form.title.data
        authorname = form.author.data
        author = get_or_create_author(authorname)
        new_book = Book(title=booktitle,author_id=author.id)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('all_books'))
    return render_template('home.html',form=form)

@app.route('/books')
def all_books():
    books = Book.query.all()
    books_and_authors = []
    for bk in books:
        info = get_book_info(bk.title)["results"]
        if len(info) > 0 and "description" in info[0]:
            desc = info[0]["description"]
        else:
            desc = "No description available"
        author = Author.query.filter_by(id=bk.author_id)
        tup = (bk.title,desc,author.name)
        books_and_authors.append(tup)
    return render_template('books.html',books_and_authors=books_and_authors)




if __name__ == "__main__":
    db.create_all()
    manager.run()
