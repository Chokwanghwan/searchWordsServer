# -*- coding:utf-8 -*-
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

urls = db.Table('urls',
    db.Column('url_id', db.Integer, db.ForeignKey('url.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

words = db.Table('words',
        db.Column('word_id', db.Integer, db.ForeignKey('word.id')),
        db.Column('url_id', db.Integer, db.ForeignKey('url.id'))
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

    def make_relationship_url(self, url):
        if not url in self.urls:
            self.urls.append(url)
            db.session.add(self)
            db.session.commit()

    @classmethod
    def get(cls, email):
        user = cls.find_by_email(email)
        if user is None:
            cls.insert_email(email)
        inserted_user = cls.find_by_email(email)

        return inserted_user

    @classmethod
    def insert_email(cls, email):
        u = User(email)
        db.session.add(u)
        db.session.commit()

    @classmethod
    def find_by_email(cls, email):
        user = cls.query.filter_by(email=email).first()
        return user

class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(200))
    words = db.relationship('Word', secondary=words,
        backref=db.backref('urls', lazy='dynamic'))

    def __init__(cls, link):
        cls.link = link

    def make_relationship_word(self, word):
        if not word in self.words:
            self.words.append(word)
            db.session.add(self)
            db.session.commit()

    @classmethod
    def get(cls, url):
        link = cls.find_by_link(url)
        if link is None:
            cls.insert_link(url)
        inserted_link = cls.find_by_link(url)
        return inserted_link

    @classmethod
    def insert_link(cls, link):
        l = Url(link)
        db.session.add(l)
        db.session.commit()

    @classmethod
    def find_by_link(cls, link):
        link = cls.query.filter_by(link=link).first()
        return link

class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    english = db.Column(db.String(20))
    mean = db.Column(db.String(20))

    def __init__(cls, english, mean):
        cls.english = english
        cls.mean = mean

    @classmethod
    def get(cls, word):
        english = word.get('english')
        mean = word.get('mean')
        word = cls.find_by_word(english)
        if word is None:
            cls.insert_word(english, mean)
        inserted_word = cls.find_by_word(english)
        return inserted_word

    @classmethod
    def insert_word(cls, english, mean):
        w = Word(english, mean)
        db.session.add(w)
        db.session.commit()

    @classmethod
    def find_by_word(cls, english):
        word = cls.query.filter_by(english=english).first()
        return word

class ReferUrl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word_book_id = db.Column(db.Integer, db.ForeignKey('word_book.id'))
    url_id = db.Column(db.Integer, db.ForeignKey('url.id'))

    def __init__(cls, word_book_id, url_id):
        cls.word_book_id = word_book_id
        cls.url_id = url_id

    @classmethod
    def get(cls, wordbook, url):
        refer_url = cls.find_by_wordbook_url(wordbook, url)
        if refer_url is None:
            cls.insert_refer_url(wordbook, url)
        refer_url = cls.find_by_wordbook_url(wordbook, url)
        return refer_url

    @classmethod
    def insert_refer_url(cls, wordbook, url):
        refer_url = ReferUrl(wordbook.id, url.id)
        db.session.add(refer_url)
        db.session.commit()

    @classmethod
    def find_by_wordbook_url(cls, wordbook, url):
        refer_url = cls.query.filter_by(word_book_id=wordbook.id, url_id=url.id).first()
        return refer_url


class WordBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    word_id = db.Column(db.Integer, db.ForeignKey('word.id'))
    is_deleted = db.Column(db.Boolean, default=False)
    refer_urls = db.relationship('ReferUrl', backref='word_book',
                                lazy='dynamic')
    
    def __init__(cls, user_id, word_id):
        cls.user_id = user_id
        cls.word_id = word_id

    def make_relationship_referurl(self, url):
        refer_url = ReferUrl.get(self, url)
        if not refer_url in self.refer_urls:
            self.refer_urls.append(refer_url)
            db.session.add(self)
            db.session.commit()

    @classmethod
    def find_by_user_word(cls, user, word):
        wb = WordBook.query.filter_by(user_id=user.id, word_id=word.id).first()
        return wb

    @classmethod
    def insert_wordbook(cls, user_id, word_id):
        wb = WordBook(user_id, word_id)
        db.session.add(wb)
        db.session.commit()

    @classmethod
    def update_wordbook(cls, update_user, update_word):
        # WordBook.update_wordbook('kwanggoo@gmail.com', {'english':'haha', 'mean':'a'})
        user_email = update_user
        user_word = update_word

        user = User.get(user_email)

        for user_word in user_word:
            word = Word.get(user_word)
            find_word_book = WordBook.query.filter_by(user_id=user.id, word_id=word.id).first()
            find_word_book.is_deleted = True
        db.session.commit()

    @classmethod
    def get(cls, user, word):
        word_book = WordBook.find_by_user_word(user, word)
        if word_book is None:
            WordBook.insert_wordbook(user.id, word.id)
        wb = WordBook.find_by_user_word(user, word)
        return wb

def searchWord(email, link, word):

    user_email = email
    user_url = link
    user_words = word

    user = User.get(user_email)
    url = Url.get(user_url)

    user.make_relationship_url(url)

    for user_word in user_words:
        word = Word.get(user_word)
        url.make_relationship_word(word)

        word_book = WordBook.get(user, word)
        word_book.make_relationship_referurl(url)

def select_word_for_web(email, link):
    # deleted_words, words = selectWord('kwanggoo@gmail.com', 'http://google.com')
    user_email = email
    user_url = link

    user = User.get(user_email)
    url = Url.get(user_url)

    deleted_word_list = []
    word_list = []
    for word in url.words:
        wb = WordBook.query.filter_by(word_id=word.id, user_id=user.id).first()        
        print '=========='
        print wb.id
        print '=========='
        if wb.is_deleted:
            deleted_word_list.append(word)
        else:
            word_list.append(word)
            
    return (deleted_word_list, word_list)

def select_word_for_mobile(email):

    user_email = email

    user = User.get(user_email)

    deleted_word_list = []
    word_list = []
    for word in user.word_books:
        w = Word.query.filter_by(id=user.id).first()
        print '=========='
        print w.english
        print w.mean
        print '=========='
        if word.is_deleted:
            deleted_word_list.append(w)
        else:
            word_list.append(w)
    return (deleted_word_list, word_list)
            











