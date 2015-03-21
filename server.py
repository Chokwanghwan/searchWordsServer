# -*- coding:utf-8 -*-

from dataControl import *

db.create_all()

@app.route('/dataControl/insertData')
# def handlerInsertData(account, recentUrl, word, mean, deleteCheck):
# 	insertData(account, recentUrl, word, mean, deleteCheck)
def referenceData(account, reqUrl, word, mean):
	#현재 사용자가 현재 방문중인 url에서 어떤 단어들을 가장 원하는지 찾아준다
	account = account
	reqUrl = reqUrl
	isAccount = User.query.filter_by(account=account).all()
	isUrl = User.query.filter_by(recentUrl=reqUrl).all()

	if isAccount != []:
		if isUrl != []:
			showData(account, reqUrl)
		else:
			insertData(account, reqUrl, word, mean, 'N')
			showData(account, reqUrl)
	else:
		insertData(account, reqUrl, word, mean, 'N')
		showData(account, reqUrl)

@app.route('/dataControl/updateData')
def handlerUpdateData(account, word):
	updateData(account, word)

if __name__ == '__main__':
	app.run()