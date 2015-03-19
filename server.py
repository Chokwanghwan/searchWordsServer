# -*- coding:utf-8 -*-

from dataControl import *

db.create_all()

@app.route('/dataControl/insertData')
def handlerInsertData(account, recentUrl, word, mean, deleteCheck):
	insertData(account, recentUrl, word, mean, deleteCheck)

@app.route('/dataControl/reference')
def handlerReferenceData(account, url):
	referenceData(account, url)

@app.route('/dataControl/updateData')
def handlerUpdateData(account, word):
	updateData(account, word)

if __name__ == '__main__':
	app.run()