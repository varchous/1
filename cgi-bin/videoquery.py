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
    qq=e.queryvid(text1)
    q1=qq[0]
    q2=qq[1]
    q3=qq[2]
except:
    pass

print("Content-type: text/html\n")
print("""<!DOCTYPE HTML>
<html>
<head>
<meta charset="utf-8">
<title>Обработка данных форм</title>
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
</head>
<body>
<a href="#" title="Вернуться к началу" class="topbutton">^Наверх</a>
    <form action="/cgi-bin/form.py">
<input type="submit" value="sites">
    </form>
    <form action="/cgi-bin/imgquery.py">
        <input type="submit" value="img">
    </form>
    <form action="/cgi-bin/videoquery.py">
	Enter query
        <input type="text" name="TEXT_1">
        <input type="submit">
    </form>
    """)
for i in q2[0]:
    if (i[0].find('embed') == -1):
        continue
    else:
        print("""<iframe width="600" height="400" src="{}" ></iframe>""".format(i[0]))
        print("<p>{}</p>".format(format(q3[0])))
        print("<br>")
print("""
</body>

</html>""")



