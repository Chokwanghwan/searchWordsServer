# -*- coding:utf-8 -*-
from flask import request, json
from models import *
import os, logging

_basedir = os.path.dirname(os.path.realpath(__file__))
_logfile = _basedir+'/../searchword.log'

logging.basicConfig(filename='/tmp/searchWords.log',level=logging.DEBUG)
# logging.debug('This message should go to the log file')
# logging.info('So should this')
# logging.warning('And this, too')

@app.route('/', methods=['GET'])
def index():
	return 'hello SearchWord'

""" 
web client의 background.js에서 본문추출하고 번역한 데이터를 
email, url과 함께 DB에 넣는 작업을 위한 url이다.
"""
@app.route('/searchWords/insertData', methods=['POST'])
def post_for_insert():
	datas = request.get_json()
	email = datas[u'email']
	url = datas[u'url']
	words = datas[u'words'].values()

	insert_data(email, url, words)
	#err이면 err사유 리턴해주고 제대로 동작했으면 ok나 카운터.
	return 'insert complete'

"""초을 클릭시 서버에 
email, url을 넘기고 그 정보로 단어를 select해서 web client에 return한다.
"""
@app.route('/searchWords/selectDataForWeb', methods=['POST'])
def post_for_select_web():
	datas = request.get_json()
	email = datas[u'email']
	url = datas[u'url']

	# email = request.values.get('email')
	# url = request.values.get('url')

	data = select_word_for_web(email, url)

	return data

"""
사용자가 mobile application 접속시 서버에 
email을 넘기고 그 정보로 단어를 select해서 mobile client에 return 한다.
"""
@app.route('/searchWords/selectDataForMobile', methods=['GET'])
def select_word_mobile():
	email = request.args.get('email')
	data = select_word_for_mobile(email)

	return data

"""
사용자가 이전에 삭제요청한 데이터를 리턴해주는 메서드
"""
@app.route('/searchWords/selectDeletedDataForMobile', methods=['GET'])
def select_deleted_word_mobile():
	email = request.args.get('email')
	data = select_delete_word_for_mobile(email)

	return data


"""
web client와 mobile client에서 서버에 
email, word를 넘기고 그 정보로 단어를 update한다. 

** return은 따로하지않고 update 결과는 DB에만 반영한다. 
** 클라이언트 단의 삭제는 클라이언트에서 해결한다.
"""
@app.route('/searchWords/updateData', methods=['POST'])
def post_for_update():
	email = request.values.get('email')
	english = request.values.get('english')
	logging.debug('updateData email is %s, english is %s'%(email, english))
	WordBook.update_wordbook(email, english)
	#client의 view에서의 삭제는 client에서 처리하므로 return 하지않음.
	return "update complete"

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')