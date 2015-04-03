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

    def __init__(cls, email):
        cls.email = email

    # @classmethod
    # def is_there_email(cls, email):
    #     user = cls.find_by_email(email)
    #     if user is None:
    #         cls.insert_user(email)
    #     inserted_user = cls.find_by_email(email)
    #     return inserted_user

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

    def __init__(cls, english, mean):
        cls.english = english
        cls.mean = mean

    @classmethod
    def insertWord(cls, english, mean):
        wb = Word(english, mean)
        db.session.add(wb)
        db.session.commit()

    @classmethod
    def find_by_word(cls, english):
        word = cls.query.filter_by(english=english).first()
        return word

class ReferUrl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word_book_id = db.Column(db.Integer, db.ForeignKey('word_book.id'))
    url_id = db.Column(db.Integer, db.ForeignKey('url.id'))

class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(120))
    words = db.relationship('Word', secondary=words,
        backref=db.backref('urls', lazy='dynamic'))

    def __init__(cls, link):
        cls.link = link

    @classmethod
    def insertLink(cls, link):
        l = Url(link)
        db.session.add(l)
        db.session.commit()

    @classmethod
    def find_by_link(cls, link):
        link = cls.query.filter_by(link=link).first()
        return link

def searchWord(email, link, word):
    userCheck = User.find_by_email(email)
    linkCheck = Url.find_by_link(link)
    wordCheck = Word.find_by_word(word)

    if userCheck is None:
        print 'email none'
        
        if linkCheck is None and wordCheck is None:
            print 'hasnot link, hasnot word'
        elif linkCheck is not None and wordCheck is None:
            print 'has link, hasnot word'
        elif linkCheck is None and wordCheck is not None:
            print 'hasnot link, has word'
        else:
            print 'has link, has word'
    else:
        print 'has email'
        
        if linkCheck is None and wordCheck is None:
            print 'hasnot link, hasnot word'
        elif linkCheck is not None and wordCheck is None:
            print 'has link, hasnot word'
        elif linkCheck is None and wordCheck is not None:
            print 'hasnot link, has word'
        else:
            print 'has link, has word'










