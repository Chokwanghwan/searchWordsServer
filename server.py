# -*- coding:utf-8 -*-

from models import *

""" 
web client의 background.js에서 본문추출하고 번역한 데이터를 
email, url과 함께 DB에 넣는 작업을 위한 url이다.
"""
@app.route('/searchWords/insertData', methods=['POST'])
def post_for_insert():
	data = []

	email = request.form['email']
	url = request.form['url']
	word = request.form['word']
	

	data = insert_data(email, url, word)

return data


"""
사용자가 chrome extension 	아이콘을 클릭시 서버에 
email, url을 넘기고 그 정보로 단어를 select해서 web client에 return한다.
"""
@app.route('/searchWords/selectDataForWeb', methods=['POST'])
def post_for_select_web():
	data = []

	email = request.form['email']	
	url = request.form['url']

	data = select_word_for_web(email, url)

	return data


"""
사용자가 mobile application 접속시 서버에 
email을 넘기고 그 정보로 단어를 select해서 mobile client에 return 한다.
"""
@app.route('/searchWords/selectDataForMobile', methods=['POST'])
def post_for_select_mobile():
	data = []

	email = request.form['email']	

	data = select_word_for_mobile(email)

	return data	


"""
web client와 mobile client에서 서버에 
email, word를 넘기고 그 정보로 단어를 update한다. 

** return은 따로하지않고 update 결과는 DB에만 반영한다. 
** 클라이언트 단의 삭제는 클라이언트에서 해결한다.
"""
@app.route('/searchWords/updateData', methods=['POST'])
def handlerUpdateData():
	data = []

	email = request.form['email']
	word = request.form['word']

	data = WordBook.update_wordbook(email, word)

	return data

if __name__ == '__main__':
	app.run
