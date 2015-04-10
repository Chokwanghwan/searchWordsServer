#!/usr/bin/env python
from models import *
db.create_all()
searchWord('kwanggoo@gmail.com', 'http://google.com', [{'english':'haha', 'mean':'a'}, {'english':'hello','mean':'b'}])
searchWord('kwanggoo@gmail.com', 'http://naver.com', [{'english':'haha', 'mean':'a'}, {'english':'naver','mean':'fuck'}])
