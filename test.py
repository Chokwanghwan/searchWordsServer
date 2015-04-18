#!/usr/bin/env python
# -*- coding:utf-8 -*-
from models import *
db.create_all()
#계정 없을때 케이스.
insert_data('kwanggoo@gmail.com', 'http://google.com', [{'english':'ghaha', 'mean':{'a', 'yt'}}, 
													   {'english':'ghello1','mean':{'a', 'yt'}}, 
													   {'english':'ghello2','mean':{'a', 'yt'}},
													   {'english':'ghello3','mean':{'a', 'yt'}},
													   {'english':'ghello4','mean':{'a', 'yt'}},
													   {'english':'ghello5','mean':{'a', 'yt'}},
													   {'english':'ghello6','mean':{'a', 't'}},
													   {'english':'ghello7','mean':{'a', 'yt'}}])

insert_data('kwanggoo@gmail.com', 'http://naver.com', [{'english':'nhaha', 'mean':{'a', 'qt'}}, 
													   {'english':'nhello1','mean':{'a', 'qt'}}, 
													   {'english':'nhello2','mean':{'a', 'qt'}},
													   {'english':'nhello3','mean':{'a', 'qt'}},
													   {'english':'nhello4','mean':{'a', 'qt'}},
													   {'english':'nhello5','mean':{'a', 'qt'}},
													   {'english':'nhello6','mean':{'a', 'qt'}},
													   {'english':'nhello7','mean':{'a', 'qt'}}])

insert_data('sunghwan@gmail.com', 'http://jojojo.com', [{'english':'nhaha', 'mean':{'a', 'tw'}}, 
													   {'english':'nhello1','mean':{'a', 'tw'}}, 
													   {'english':'nhello2','mean':{'a', 'tw'}},
													   {'english':'nhello3','mean':{'a', 'tw'}},
													   {'english':'nhello4','mean':{'a', 'tw'}},
													   {'english':'nhello5','mean':{'a', 'tw'}},
													   {'english':'nhello6','mean':{'a', 'tw'}},
													   {'english':'nhello7','mean':{'a', 'tw'}}])


insert_data('sunghwan@gmail.com', 'http://jojojo.com', [{'english':'ssnhaha', 'mean':{'a', 'tq'}}, 
													   {'english':'ssnhello1','mean':{'a', 'tq'}}, 
													   {'english':'ssnhello2','mean':{'a', 'tq'}},
													   {'english':'ssnhello3','mean':{'a', 'tq'}},
													   {'english':'ssnhello4','mean':{'a', 'tq'}},
													   {'english':'ssnhello5','mean':{'a', 'tq'}},
													   {'english':'ssnhello6','mean':{'a', 'tq'}},
													   {'english':'ssnhello7','mean':{'a', 'tq'}}])

insert_data('kwanggoo@gmail.com', 'http://yahoo.com', [{'english':'yhaha', 'mean':{'a', 'tz'}}, 
													   {'english':'yhello1','mean':{'a', 'tz'}}, 
													   {'english':'yhello2','mean':{'a', 'tz'}},
													   {'english':'yhello3','mean':{'a', 'tz'}},
													   {'english':'yhello4','mean':{'a', 'tz'}},
													   {'english':'yhello5','mean':{'a', 'tz'}},
													   {'english':'yhello6','mean':{'a', 'tz'}},
													   {'english':'yhello7','mean':{'a', 'tz'}}])

insert_data('kwanggoo@gmail.com', 'http://d.android.com', [{'english':'dhaha', 'mean':{'a', 't'}}, 
													   {'english':'dhello1','mean':{'a', 'tv'}}, 
													   {'english':'dhello2','mean':{'a', 'tv'}},
													   {'english':'dhello3','mean':{'a', 'tv'}},
													   {'english':'dhello4','mean':{'a', 'tv'}},
													   {'english':'dhello5','mean':{'a', 'tv'}},
													   {'english':'dhello6','mean':{'a', 'tv'}},
													   {'english':'dhello7','mean':{'a', 'tv'}}])

insert_data('kwanggoo@gmail.com', 'http://good_jeju.com', [{'english':'jhaha', 'mean':{'a', 't'}}, 
													   {'english':'jhello1','mean':{'a', 'tx'}}, 
													   {'english':'jhello2','mean':{'a', 'tx'}},
													   {'english':'jhello3','mean':{'a', 'tx'}},
													   {'english':'jhello4','mean':{'a', 'tx'}},
													   {'english':'jhello5','mean':{'a', 'tx'}},
													   {'english':'jhello6','mean':{'a', 'tx'}},
													   {'english':'jhello7','mean':{'a', 'tx'}}])