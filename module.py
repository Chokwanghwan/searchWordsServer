# -*- coding:utf-8 -*-
import urllib2
import re
import json
import requests
import sys
import datetime
from operator import itemgetter

from models import *
from logging.handlers import RotatingFileHandler

"""
1. html 소스 추출 후 공백 제거
2. javascript 소스 제거
3. 모든 html tag 제거
4. 단어 추출
5. 번역
6. 단어 포멧 변경 후 insert DB
"""
#1
#https << handshake Fail 에러 발생
def htmlParsing(url):
	response = urllib2.urlopen(url)
	page_source = response.read()
	return page_source

def extractContent(page_source):
	code = [line.strip() for line in page_source.split('\n') if line.strip() != '']
	data = ''.join(code)
	data = re.sub(r'\<!--.*?-->', '', data)
	data = re.sub(r'\<head.*?</head>', '', data)
	data = re.sub(r'\<title.*?</title>', '', data)
	data = re.sub(r'\<style.*?</style>', '', data)
	data = re.sub(r'\<script.*?</script>', '', data)
	data = re.sub(r'\<pre.*?</pre>', '', data)
	data = re.sub(r'&nbsp;', '', data)
	data = re.sub(r'[\d]', '', data)
	data = re.sub(r'\b\w\b', '', data)
	p = re.compile(r'<.*?>')
	data = p.sub('', data)	
	data = data.split(' ')	
	return data

def translateWords(data):
	# keyCount = 0
	# a = ['hello', 'bye', 'fuck', 'home', 'hoho', 'bye', 'bye', '123123', '안녕하세요']
	wordList = []
	for i in data:
		data = re.sub(r'[\.]', '', i)	
		data = re.sub(r'[^a-zA-Z]', '', i)
		if not data is '':
			url = "http://tooltip.dic.naver.com/tooltip.nhn?wordString="+i+"&languageCode=4&nlp=false";
			request = requests.get(url)
			result = request.text
			# response = urllib2.urlopen(url)
			result = json.loads(result)
			# keyCount = keyCount+1
			if ('entryName' in result):
				english = result['entryName']
				mean = result['mean']
				# print english
				# print mean
				if (not english in wordList):
					wordList.append({'english': english, 'mean': mean})
			# if keyCount == len(a):
			# 	print 'complete'
	return wordList

def insert_data(email, link, words):
	user = User.get(email)
	url = Url.get(link)

	user.make_relationship_url(url)

	for user_word in words:
		if not user_word is None:
			english = user_word.get('english')
			mean = user_word.get('mean')
			mean = ','.join(mean)
			word = Word.get(english, mean)
			url.make_relationship_word(word)

			word_book = WordBook.get(user, word)
			word_book.make_relationship_referurl(url)

def words_list_sorted(words):
	sorted_words = sorted(words, key=itemgetter('urls'),reverse=True)
	return sorted_words

def timeCheck(flag, x):
	d = datetime.datetime.now()
	if x is 1:
		return d
	else:
		return d

def select_word_for_web(email, link):
	methodX = timeCheck("메서드 시작", 1)
	user = User.get(email)
	url = Url.get(link)

	deleted_word_list = []
	word_list = []
	app.logger.info("web select user = %s", email)
	app.logger.info("web select url = %s", link)
	forX = timeCheck("분기문 시작", 1)
	for word in url.words:
		if not word is None:
			wbX = timeCheck("wb", 1)
			wb = WordBook.query.first()
			wbY = timeCheck("wb", 2)
			print("wb 경과시간 : " + str(wbY-wbX))
			if wb is None:
				continue
			else:
				wX = timeCheck("w", 1)
				w = Word.query.filter_by(id=wb.word_id).first()
				wY = timeCheck("w", 2)
				print("w 경과시간 : " + str(wY-wX))

				# url_countX = timeCheck("w", 1)
				# url_count = len(wb.refer_urls)
				# url_countY = timeCheck("w", 2)
				# print("url_count 경과시간 : " + str(url_countY-url_countX))
				english = w.english
				mean = w.mean.split(',')

				# words = {'english': english, 'mean': mean, 'urls':url_count}
				words = {'english': english, 'mean': mean}
				if wb.is_deleted:
					deleted_word_list.append(words)
				else:
					word_list.append(words)
	forY = timeCheck("분기문 종료", 2)	
	print("반복문 수행 시간 : " + str(forY-forX))
	print(forY-forX)
	app.logger.info("web select word len = %d", len(word_list))
	word_list = words_list_sorted(word_list)
	word_list = json.dumps(word_list)
	methodY = timeCheck("메서드 종료", 2)
	print("메서드 전체 수행 시간 : " + str(methodY-methodX))
	return word_list	

def select_word_for_mobile(email):
	user = User.get(email)
	word_list = []
	app.logger.info("mobile select user = %s", email)
	old = datetime.now()
	for wb in user.word_books.filter_by(is_deleted=False).all():
		w = Word.query.filter_by(id=wb.word_id).first()
		english = w.english
		mean = w.mean
		words = {'english': english, 'mean': mean, 'urls':len(wb.refer_urls.all())}
		word_list.append(words)
	
	current = datetime.now()
	lapse = current - old
	app.logger.info("laps = %s", lapse.__str__())
	app.logger.info("mobile select word len = %d", len(word_list))
	word_list = words_list_sorted(word_list)
	word_list = json.dumps(word_list)
	return word_list

def select_delete_word_for_mobile(email):
	user = User.get(email)

	deleted_word_list = []
	for wb in user.word_books.filter_by(is_deleted=True).all():
		w = Word.query.filter_by(id=wb.word_id).first()
		english = w.english
		mean = w.mean

		words = {'english': english, 'mean': mean, 'urls':len(wb.refer_urls.all())}
		deleted_word_list.append(words)
	word_list = words_list_sorted(deleted_word_list)
	deleted_word_list = json.dumps(deleted_word_list)
	return deleted_word_list

def find_user_info(email):
	user = User.get(email)

	all_word_count = len(user.word_books.all())
	deleted_word_count = len(user.word_books.filter_by(is_deleted=True).all())
	url_count = len(user.urls)

	count = {'all_word_count': all_word_count, 'deleted_word_count': deleted_word_count, 'url_count': url_count}
	return json.dumps(count)

def find_all_words():
	all_words_list = []
	for w in Word.query.all():
		word = {'english': w.english, 'mean': w.mean}
		all_words_list.append(word)
	return json.dumps(all_words_list)











