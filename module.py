# -*- coding:utf-8 -*-
import urllib2
import re
import json
import requests

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
	return json.dumps(wordList)