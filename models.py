# -*- coding:utf-8 -*-
from flask import Flask, json
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.dialects import postgresql

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/searchWords.db'
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
            dbException()

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
        dbException()

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
            dbException()

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
        dbException()

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
    def get(cls, english, mean):
        word = cls.find_by_word(english)
        if word is None:
            cls.insert_word(english, mean)
        inserted_word = cls.find_by_word(english)
        return inserted_word

    @classmethod
    def insert_word(cls, english, mean):
        w = Word(english, mean)
        db.session.add(w)
        dbException()

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
        dbException()

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
            dbException()

    @classmethod
    def find_by_user_word(cls, user, word):
        wb = WordBook.query.filter_by(user_id=user.id, word_id=word.id).first()
        return wb

    @classmethod
    def insert_wordbook(cls, user_id, word_id):
        wb = WordBook(user_id, word_id)
        db.session.add(wb)
        dbException()

    @classmethod
    def update_wordbook(cls, email, english, is_deleted):
        user = User.get(email)

        find_english = Word.find_by_word(english)
        find_word_book = WordBook.query.filter_by(user_id=user.id, word_id=find_english.id).first()

        find_word_book.is_deleted = is_deleted
        dbException()

    @classmethod
    def get(cls, user, word):
        word_book = WordBook.find_by_user_word(user, word)
        if word_book is None:
            WordBook.insert_wordbook(user.id, word.id)
        wb = WordBook.find_by_user_word(user, word)
        return wb

def dbException():
    failed=False
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        failed=True

def insert_data(email, link, words):
    user = User.get(email)
    url = Url.get(link)

    user.make_relationship_url(url)

    for user_word in words:
        english = user_word.get('english')
        mean = user_word.get('mean')
        mean = ','.join(mean)
        word = Word.get(english, mean)
        url.make_relationship_word(word)

        word_book = WordBook.get(user, word)
        word_book.make_relationship_referurl(url)

def select_word_for_web(email, link):
    user = User.get(email)
    url = Url.get(link)

    deleted_word_list = []
    word_list = []

    for word in url.words:
        wb = WordBook.query.filter_by(user_id=user.id, word_id=word.id).first()
        w = Word.query.filter_by(id=wb.word_id).first()
        english = w.english
        mean = w.mean.split(',')

        words = {'english': english, 'mean': mean}
        if wb.is_deleted:
            deleted_word_list.append(words)
        else:
            word_list.append(words)
    
    word_list = json.dumps(word_list)        
    return word_list

def select_word_for_mobile(email):
    user = User.get(email)

    word_list = []
    for word in user.word_books:
        w = Word.query.filter_by(id=word.id).first()
        english = w.english
        mean = w.mean

        words = {'english': english, 'mean': mean}
        if not word.is_deleted:
            word_list.append(words)
    word_list = json.dumps(word_list)
    return word_list

def select_delete_word_for_mobile(email):
    user = User.get(email)

    deleted_word_list = []
    for word in user.word_books:
        w = Word.query.filter_by(id=word.id).first()
        english = w.english
        mean = w.mean

        words = {'english': english, 'mean': mean}
        if word.is_deleted:
            deleted_word_list.append(words)
    deleted_word_list = json.dumps(deleted_word_list)
    return deleted_word_list

def find_user_info(email):
    user = User.get(email)

    all_word_count = len(user.word_books.all())
    deleted_word_count = len(user.word_books.filter_by(is_deleted=True).all())
    url_count = len(user.urls)

    count = {'all_word_count': all_word_count, 'deleted_word_count': deleted_word_count, 'url_count': url_count}
    return json.dumps(count)
    












