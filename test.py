#! /usr/bin/env python
# -*- coding: utf-8 -*-
import crawlerfile
import imp
import urllib
import urllib.request
import os
#from BeautifulSoup import *
from bs4 import BeautifulSoup
#from urlparse import urljoin
from urllib.parse import urljoin
from urllib.parse import urlparse
#import psycopg2
import postgresql
import sqlite3
#from pysqlite2 import dbapi2 as sqlite
#reload(crawler)
#import sys
#import nn
#reload(sys)
#sys.setdefaultencoding('utf-8')
ignorewords=set(['the','of','to','and','a','in','is','it'])


#c=urllib.request.urlopen('http://dontabak.com.ua/')
#print (c.read())
#imp.reload(crawlerfile)
#crawler=crawlerfile.crawler('searchindex.db')
#crawler.createvid()
#imp.reload(crawlerfile)
#crawler=crawlerfile.img('searchindex.db')
#crawler.create()
#---------------------------- работа паука
"""
crawler=crawlerfile.crawler('searchindex.db')
pages= ['http://server.odessa.ua/']
crawler.crawl(pages)
"""
#------------------------- Запрос
"""
e=crawlerfile.searcher('searchindex.db')
qq=e.query(u'дыня')
qqq=qq[1]
qqq3=qq[3]
print (qqq3[0])
#print(e.geturlname(qqq[3]))
"""
"""
e=crawlerfile.searcher('searchindex.db')
q1=e.queryvid('BadComedian')
qqq=q1[1]
q2=q1[1]
for i in q2[0]:
    if(i[0].find('embed')!=-1):
        print (i[0])
    else:
        print('bert')



"""
"""
crawler=crawlerfile.crawler('searchindex.db')
pages= ['https://www.youtube.com/watch?v=os2HYtR186o']
crawler.crawlvid(pages)
"""
#------------------------Вывод таблицы
"""
con = sqlite3.connect('searchindex.db')
with con:
    cur = con.cursor()
    #cur.execute("Insert into wordlist(word) values ('привет')")
    cur.execute("SELECT * FROM title ")
    rows = cur.fetchall()
    for row in rows:
        print (row[0])
    #k=rows[20953]
    #print k[0]
"""
#---------------------------Вычисление PageRank
#"""
crawler=crawlerfile.crawler('searchindex.db')
crawler.calculatepagerank( )
#cur=crawler.con.execute('select * from pagerank order by score desc')
#"""
#------------------------Вывод ссылки
"""""
with con:
    cur = con.cursor()
    cur.execute("SELECT * FROM urllist where rowid=1")
    rows = cur.fetchall()

    for row in rows:
        print row
"""""



"""# POSTGRESQL
conn_string = "host='localhost' dbname='Test' user='postgres' password='secret'"
print "Connecting to database\n	->%s" % (conn_string)
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()
namedict = ({"name":"Joshua", "age":"2"},
            {"name":"Steven", "age":"1"},
            {"name":"David", "age":"3"})
try:
    cursor.executemany("INSERT INTO testtable(name,age) VALUES (%(name)s, %(age)s)", namedict)
except:
    print "I can't INSERT INTO testtable"
try:
    cursor.execute("SELECT name from testtable")
except:
    print "I can't SELECT from testtable"
rows = cursor.fetchall()
for row in rows:
    print row
"""


"""import re
text= u"привет C++ b2ye bye"
pattern = re.compile(u"[^a-zа-я]")
result = [s.lower() for s in pattern.split(text) if s != '']
result2 =pattern.findall(text)
for i in result:
    print i,"-"
print len(result)
for i in result2:
    print i
"""

