# -*- coding:utf-8 -*-
import urllib2
import re
import json
import requests
import sys
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

		words = {'english': english, 'mean': mean, 'urls':len(wb.refer_urls.all())}
		if wb.is_deleted:
			deleted_word_list.append(words)
		else:
			word_list.append(words)
	word_list = words_list_sorted(word_list)
	word_list = json.dumps(word_list)        
	return word_list

def select_word_for_mobile(email):
	user = User.get(email)
	app.logger.info(email)
	word_list = []
	for word in user.word_books:

		w = Word.query.filter_by(id=word.id).first()
		english = w.english
		mean = w.mean

		words = {'english': english, 'mean': mean, 'urls':len(word.refer_urls.all())}
		if not word.is_deleted:
			word_list.append(words)
	word_list = words_list_sorted(word_list)
	word_list = json.dumps(word_list)
	app.logger.info(word_list)
	return word_list

def select_delete_word_for_mobile(email):
	user = User.get(email)

	deleted_word_list = []
	for word in user.word_books:
		w = Word.query.filter_by(id=word.id).first()
		english = w.english
		mean = w.mean

		words = {'english': english, 'mean': mean, 'urls':len(word.refer_urls.all())}
		if word.is_deleted:
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