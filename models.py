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

def renewWords(english, link):
    linkInfo = Url.findByLink(link)
    wordInfo = Word.findByWord(english)

    linkInfo.words.append(wordInfo)
    db.session.add(linkInfo)
    db.session.commit()

    print wordInfo.id
    print linkInfo.id

def renewUrls(email, link):
    userInfo = User.findByEmail(email)
    linkInfo = Url.findByLink(link)

    userInfo.urls.append(linkInfo)
    db.session.add(userInfo)
    db.session.commit()

    print userInfo.id
    print linkInfo.id

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
            self.urls.append(linkInfo)
            db.session.add(self)
            db.session.commit()

    @classmethod
    def insertUser(cls, email):
        u = User(email)
        db.session.add(u)
        db.session.commit()

    @classmethod
    def findByEmail(cls, email):
        user = cls.query.filter_by(email=email).first()
        return user

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
        w = Word(english, mean)
        db.session.add(w)
        db.session.commit()

    @classmethod
    def findByWord(cls, english):
        word = cls.query.filter_by(english=english).first()
        return word

class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(120))
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
    def insertLink(cls, link):
        l = Url(link)
        db.session.add(l)
        db.session.commit()

    @classmethod
    def findByLink(cls, link):
        link = cls.query.filter_by(link=link).first()
        return link


class ReferUrl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word_book_id = db.Column(db.Integer, db.ForeignKey('word_book.id'))
    url_id = db.Column(db.Integer, db.ForeignKey('url.id'))

    def __init__(cls, wordBookId, linkId):
        cls.wordBookId = wordBookId
        cls.linkId = linkId

    @classmethod
    def renewReferUrl(cls, wordBookId, linkId):
        ru = ReferUrl(wordBookId, linkId)
        db.session.add(ru)
        db.session.commit()
    # @classmethod
    # def findByReferUrl(cls, linkId):

class WordBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    word_id = db.Column(db.Integer, db.ForeignKey('word.id'))
    refer_urls = db.relationship('ReferUrl', backref='word_book',
                                lazy='dynamic')
    
    def __init__(cls, userId, wordId):
        cls.userId = userId
        cls.wordId = wordId

    def make_relationship_referurl(self, url):
        refer_url = ReferUrl.get(self, url)
        if not refer_url in self.refer_urls:
            self.refer_urls.append(refer_url)

    @classmethod
    def renewWordBook(cls, userId, wordId):
        wb = WordBook(userId, wordId)
        db.session.add(wb)
        db.session.commit()

    @classmethod
    def find_by_user_word(cls, user, word):
        wb = WordBook.query.filter_by(user_id=user.id, word_id=word.id).first()
        return wb

    @classmethod
    def get(cls, user, word):
        word_book = WordBook.find_by_user_word(user, word)
        if word_book is None:
            WordBook.renewWordBook(user.id, word.id)
        wb = WordBook.find_by_user_word(user, word)
        return wb

def searchWord(email, link, word):
    # userCheck = User.findByEmail(email)
    # linkCheck = Url.findByLink(link)
    # wordCheck = Word.findByWord(word)

    # print userCheck.id
    # print linkCheck.id
    # print wordCheck.id

    # user가 있나 없나 체크.
    user_email = "hello@world.com"
    user_url = "http://www.google.com"
    user_words = [word1, word2]

    #User.get()은 항상 User를 반환한다. (유저가 있으면 넣고 없으면 생성한후 반환)
    user = User.get(user_email)
    url = Url.get(user_url)

    user.make_relationship_url(url)

    for user_word in user_words:
        word = Word.get(word)
        url.make_relationship_word(word)

        word_book = WordBook.get(user, word)
        word_book.make_relationship_referurl(url)


    # if userCheck is None:
    #     print 'email none'
    #     if linkCheck is None and wordCheck is None:
    #         print 'hasnot link, hasnot word'
    #         #4
    #     elif linkCheck is not None and wordCheck is None:
    #         print 'has link, hasnot word'
    #         # 3
    #     elif linkCheck is None and wordCheck is not None:
    #         print 'hasnot link, has word'
    #         # 2
    #     else:
    #         print 'has link, has word'
    #         # 1
    # else:
    #     print 'has email'
    #     if linkCheck is None and wordCheck is None:
    #         print 'hasnot link, hasnot word'
    #         #4
    #     elif linkCheck is not None and wordCheck is None:
    #         print 'has link, hasnot word'
    #         #3
    #     elif linkCheck is None and wordCheck is not None:
    #         print 'hasnot link, has word'
    #         #2
    #     else:
    #         print 'has link, has word'
    #         #1


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
    case2 = {'email':email1, 'link':link2, 'words':[word1, word2]}
    case3 = {'email':email1, 'link':link1, 'words':[word1, word2]}
    case4 = {'email':email1, 'link':link2, 'words':[word1, word2]}
    case5 = {'email':email2, 'link':link3, 'words':[word1, word2]}
    case6 = {'email':email2, 'link':link4, 'words':[word1, word2]}
    case7 = {'email':email2, 'link':link3, 'words':[word1, word2]}
    case8 = {'email':email2, 'link':link4, 'words':[word1, word2]}








