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
    deleteCheck = db.Column(db.String(2)
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
    def get(cls, user, word):
        word_book = WordBook.find_by_user_word(user, word)
        if word_book is None:
            WordBook.insert_wordbook(user.id, word.id)
        wb = WordBook.find_by_user_word(user, word)
        return wb

def searchWord(email, link, word):

    # user가 있나 없나 체크.
    user_email = email
    user_url = link
    # user_words = [{'hello':'a'}, {'bye':'b'}]
    user_words = word

    #User.get()은 항상 User를 반환한다. (유저가 있으면 넣고 없으면 생성한후 반환)
    user = User.get(user_email)
    url = Url.get(user_url)

    user.make_relationship_url(url)

    for user_word in user_words:
        word = Word.get(user_word)
        url.make_relationship_word(word)

        word_book = WordBook.get(user, word)
        word_book.make_relationship_referurl(url)

def testData():
    email1 = 'kwanggoo@gmail.com'
    email2 = 'sunghwan@gmail.com'
    link1 = 'http://google.com'
    link2 = 'http://naver.com'
    link3 = 'http://yahoo.com'
    link4 = 'http://android.com'
    eng1 = 'haha'
    eng2 = 'hell'
    eng3 = 'meet'
    eng4 = 'yet'
    mean1 = 'a'
    mean2 = 'b'
    mean3 = 'c'
    mean4 = 'd'

    word1 = {'english':eng1, 'mean':mean1}
    word2 = {'english':eng2, 'mean':mean2}
    word3 = {'english':eng3, 'mean':mean3}
    word4 = {'english':eng4, 'mean':mean4}
    
    # case1 = {'email':email1, 'link':link1, 'words':[{'english':eng1, 'mean':mean1}, {'english':eng2, 'mean':mean2}]}
    # case2 = {'email':email1, 'link':link2, 'english':eng1, 'mean':mean1}
    # case3 = {'email':email1, 'link':link1, 'english':eng2, 'mean':mean2}
    # case4 = {'email':email1, 'link':link2, 'english':eng2, 'mean':mean2}
    # case5 = {'email':email2, 'link':link3, 'english':eng3, 'mean':mean3}
    # case6 = {'email':email2, 'link':link4, 'english':eng3, 'mean':mean3}
    # case7 = {'email':email2, 'link':link3, 'english':eng4, 'mean':mean4}
    # case8 = {'email':email2, 'link':link4, 'english':eng4, 'mean':mean4}

    case1 = {'email':email1, 'link':link1, 'words':[word1, word2]}
    case2 = {'email':email1, 'link':link2, 'words':[word2, word3]}
    case3 = {'email':email1, 'link':link1, 'words':[word3, word4]}
    case4 = {'email':email1, 'link':link2, 'words':[word4, word1]}
    case5 = {'email':email2, 'link':link3, 'words':[word1, word2]}
    case6 = {'email':email2, 'link':link4, 'words':[word2, word3]}
    case7 = {'email':email2, 'link':link3, 'words':[word3, word4]}
    case8 = {'email':email2, 'link':link4, 'words':[word4, word1]}