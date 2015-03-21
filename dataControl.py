# -*- coding:utf-8 -*-

from models import *

def insertData(account, recentUrl, word, mean, deleteCheck):
	account = account
	recentUrl = recentUrl
	word = word
	mean = mean
	deleteCheck = deleteCheck

	namnam = User(account, recentUrl, word, mean, deleteCheck)

	try:
		db.session.add(namnam)
		db.session.commit()
	except:
		db.session.rollback()
	finally:
		db.session.close()

	users = User.query.all()
	# admin = User.query.filter_by(username='haha').all()
	print users

	print '============================'

def showData(account, reqUrl):
	#테스트를 위해서 그냥 account과 url모두가 일치하고 deleteCheck가 'N'인 
	#놈의 word와 mean을 출력할것. 원래라면 클라이언트에 보내줘야함.
	account = account
	reqUrl = reqUrl
	
	datas = User.query.filter_by(account=account, recentUrl=reqUrl, deleteCheck='N').all()
	for i in datas:
		print i.word + ' : ' + i.mean

 
def updateData(account, word):
	account = account
	word = word
	#현재 사용자가 삭제요청을 한 단어를받아서 deleteCheck를 수정한다.
	db.session.query(User).update({Stuff.foo: Stuff.foo + 1})
	db.session.commit()
	return users








