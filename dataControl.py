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
	select = User.query.filter_by(account = 'd').all()
	print users

	print '====================='
	print select
	print '====================='

def updateData(account, word):
	account = account
	word = word
	#현재 사용자가 삭제요청을 한 단어를받아서 deleteCheck를 수정한다.
	db.session.query(User).update({Stuff.foo: Stuff.foo + 1})
	db.session.commit()
	return users		

def referenceData(account, reqUrl):
	account = account
	reqUrl = reqUrl
	print account
	print reqUrl
	#현재 사용자가 현재 방문중인 url에서 어떤 단어들을 가장 원하는지 찾아준다
	showInfo = User.query.filter_by(account=account, recentUrl=reqUrl).all()
	# show = User.query.all()
	print showInfo