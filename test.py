#!/usr/bin/env python
# -*- coding:utf-8 -*-
from models import *
db.create_all()
#계정 없을때 케이스.
searchWord('kwanggoo@gmail.com', 'http://google.com', [{'english':'ghaha', 'mean':'a'}, 
													   {'english':'ghello1','mean':'b'}, 
													   {'english':'ghello2','mean':'b'},
													   {'english':'ghello3','mean':'b'},
													   {'english':'ghello4','mean':'b'},
													   {'english':'ghello5','mean':'b'},
													   {'english':'ghello6','mean':'b'},
													   {'english':'ghello7','mean':'b'}])

searchWord('kwanggoo@gmail.com', 'http://naver.com', [{'english':'nhaha', 'mean':'a'}, 
													   {'english':'nhello1','mean':'b'}, 
													   {'english':'nhello2','mean':'b'},
													   {'english':'nhello3','mean':'b'},
													   {'english':'nhello4','mean':'b'},
													   {'english':'nhello5','mean':'b'},
													   {'english':'nhello6','mean':'b'},
													   {'english':'nhello7','mean':'b'}])

searchWord('sunghwan@gmail.com', 'http://jojojo.com', [{'english':'nhaha', 'mean':'a'}, 
													   {'english':'nhello1','mean':'b'}, 
													   {'english':'nhello2','mean':'b'},
													   {'english':'nhello3','mean':'b'},
													   {'english':'nhello4','mean':'b'},
													   {'english':'nhello5','mean':'b'},
													   {'english':'nhello6','mean':'b'},
													   {'english':'nhello7','mean':'b'}])


searchWord('sunghwan@gmail.com', 'http://jojojo.com', [{'english':'ssnhaha', 'mean':'a'}, 
													   {'english':'ssnhello1','mean':'b'}, 
													   {'english':'ssnhello2','mean':'b'},
													   {'english':'ssnhello3','mean':'b'},
													   {'english':'ssnhello4','mean':'b'},
													   {'english':'ssnhello5','mean':'b'},
													   {'english':'ssnhello6','mean':'b'},
													   {'english':'ssnhello7','mean':'b'}])

searchWord('kwanggoo@gmail.com', 'http://yahoo.com', [{'english':'yhaha', 'mean':'a'}, 
													   {'english':'yhello1','mean':'b'}, 
													   {'english':'yhello2','mean':'b'},
													   {'english':'yhello3','mean':'b'},
													   {'english':'yhello4','mean':'b'},
													   {'english':'yhello5','mean':'b'},
													   {'english':'yhello6','mean':'b'},
													   {'english':'yhello7','mean':'b'}])

searchWord('kwanggoo@gmail.com', 'http://d.android.com', [{'english':'dhaha', 'mean':'a'}, 
													   {'english':'dhello1','mean':'b'}, 
													   {'english':'dhello2','mean':'b'},
													   {'english':'dhello3','mean':'b'},
													   {'english':'dhello4','mean':'b'},
													   {'english':'dhello5','mean':'b'},
													   {'english':'dhello6','mean':'b'},
													   {'english':'dhello7','mean':'b'}])

searchWord('kwanggoo@gmail.com', 'http://good_jeju.com', [{'english':'jhaha', 'mean':'a'}, 
													   {'english':'jhello1','mean':'b'}, 
													   {'english':'jhello2','mean':'b'},
													   {'english':'jhello3','mean':'b'},
													   {'english':'jhello4','mean':'b'},
													   {'english':'jhello5','mean':'b'},
													   {'english':'jhello6','mean':'b'},
													   {'english':'jhello7','mean':'b'}])