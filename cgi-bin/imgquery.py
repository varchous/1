#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cgi
import sys
import codecs
import html
import crawlerfile
import imp
import urllib
import urllib.request
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlparse
import postgresql
import sqlite3
ignorewords=set(['the','of','to','and','a','in','is','it'])
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

form = cgi.FieldStorage()
text1 = form.getfirst("TEXT_1", "не задано")
text1=text1.lower()
#text2 = form.getfirst("TEXT_2", "не задано")
text1 = html.escape(text1)
#text2 = html.escape(text2)

e=crawlerfile.searcher('searchindex.db')
try:
    qq=e.queryimg(text1)
    print (qq[0][0])
except:
    pass
print("Content-type: text/html\n")
print("""<!DOCTYPE HTML>
<html>
<head>
<style type="text/css">

.topbutton {
width:100px;
border:2px solid #ccc;
background:#f7f7f7;
text-align:center;
padding:10px;
position:fixed;
bottom:50px;
right:50px;
cursor:pointer;
color:#333;
font-family:verdana;
font-size:12px;
border-radius: 5px;
-moz-border-radius: 5px;
-webkit-border-radius: 5px;
-khtml-border-radius: 5px;
}
</style>
<meta charset="utf-8">
<title>Обработка данных форм</title>
</head>
<body>
<a href="#" title="Вернуться к началу" class="topbutton">^Наверх</a>
    <form action="/cgi-bin/form.py">
        <input type="submit" value="sites">
    </form>
        <form action="/cgi-bin/videoquery.py" >
        <input type="submit" value="video">
    </form>
    <form action="/cgi-bin/imgquery.py">
	Enter query
        <input type="text" name="TEXT_1">
        <input type="submit">
    </form>
    <br>
    """)
#print("<p>TEXT_1:</p>")
#print("<p>TEXT_1: {}</p>".format(e.queryimg(text1)[1]))
for i in range(len(qq)):
    print("<div style='float:left'>")
    print("""<a href="{}"><img src="{}" width="255" height="255"  style='float:left'></a>""".format(qq[i][0],qq[i][0]))
    print("<br>")
    print("""<a href="{}">Перейти на страницу</a>""".format(qq[i][1]))
    print("</div>")
print("</body> </html>")
#print(text1)


