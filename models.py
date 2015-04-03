from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

urls = db.Table('urls',
    db.Column('url_id', db.Integer, db.ForeignKey('url.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(45))
    # password = db.Column(db.String(32))

    word_books = db.relationship('WordBook', backref='user',
                                lazy='dynamic')
    urls = db.relationship('Url', secondary=urls,
        backref=db.backref('users', lazy='dynamic'))
    
    def __init__(self, email):
        self.email = email

    @classmethod
    def fuck_up(cls, email):
        user = cls.find_by_email(email)
        if user is None:
            cls.insert_user(email)
        inserted_user = cls.find_by_email(email)
        return inserted_user

    @classmethod
    def insert_user(cls, email):
        u = User(email)
        db.session.add(u)
        db.session.commit()

    @classmethod
    def find_by_email(cls, email):
        user = cls.query.filter_by(email=email).first()
        return user

class WordBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    word_id = db.Column(db.Integer, db.ForeignKey('word.id'))
    refer_urls = db.relationship('ReferUrl', backref='word_book',
                                lazy='dynamic')

words = db.Table('words',
        db.Column('word_id', db.Integer, db.ForeignKey('word.id')),
        db.Column('url_id', db.Integer, db.ForeignKey('url.id'))
)

# user []
# link []
# words [][][][][][][][]

class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    english = db.Column(db.String(20))
    mean = db.Column(db.String(20))

    def __init__(self, english, mean):
        self.english = english
        self.mean = mean

class ReferUrl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word_book_id = db.Column(db.Integer, db.ForeignKey('word_book.id'))
    url_id = db.Column(db.Integer, db.ForeignKey('url.id'))

class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(120))
    words = db.relationship('Word', secondary=words,
        backref=db.backref('urls', lazy='dynamic'))

    def __init__(self, link):
        self.link = link

#insert english, mean in Word table
def insertWordData(english, mean):

    wordInfo = Word(english, mean)

    try:
        db.session.add(wordInfo)
        # db.session.add(wordBookInput)
        # db.session.add(urlInput)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()

    # users = Word.query.all()
    # admin = User.query.filter_by(username='haha').all()
    # print users

    print '============================'            


#insert account in User table
def insertUserData(email):
    print email
    
    userInfo = User(email)


    try:
        db.session.add(userInfo)
        # db.session.add(wordBookInput)
        # db.session.add(urlInput)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()

    # users = User.query.all()
    # admin = User.query.filter_by(username='haha').all()
    # print users

    print '============================'            