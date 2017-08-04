#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cgi
import sys
import codecs
import html
import crawlerfile
import http.cookies
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
    qq=e.query(text1)
    qqq=qq[1]
    qqq3=qq[2]
    qqq4=qq[3]
except:
    pass
#print (qqq[0])
#print(e.geturlname(qqq[0]))
#ee=e.query(text1)
print("Content-type: text/html\n")


print("""<!DOCTYPE HTML>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Обработка данных форм</title>
            <script type="text/javascript">
                function reloadPage()
                {
                    window.location.reload()
                }
            </script>
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
<link rel="stylesheet" media="screen,projection" href="/css/ui.totop.css" />
        </head>
        <body>

        <a href="#" title="Вернуться к началу" class="topbutton">^Наверх</a>

    """)
print("""
<div>

<form action="/cgi-bin/imgquery.py" >
        <input type="submit" value="img">
    </form>
    <form action="/cgi-bin/videoquery.py" >
        <input type="submit" value="video">
    </form>
    <form action="/cgi-bin/form.py">
	Enter query
        <input type="text" name="TEXT_1">
        <input type="submit">
    </form>
</div>


""")
#ee=e.query(text1)
print("<p>{}</p>".format(len(qq[1])))

for i in range(len(qq[1])):
    print("<br>")
    if(qqq3[i]!= None):
        print("<p>{}</p>".format(qqq3[i][0]))
    print("<a href=""{}"">{}</a>".format(e.geturlname(qqq[i]),e.geturlname(qqq[i])))
    if(qqq4[i] != None):
        print("<p>{}</p>".format(qqq4[i][0]))
    print("<br>")

#print("<p>",e.query(text1),"</p>")
#print("<p>TEXT_2: {}</p>".format(text2))
#print("""<img src="http://dontabak.com.ua/3289-home_default/ugol-kokosovyj-tom-cococha-gold-1kg-72-sht-bolshoj-kubik.jpg" alt="альтернативный текст">""")
#print("""<iframe width="600" height="400" src="https://www.youtube.com/embed/cbLlTiJTay0" ></iframe>""")
print("""</body>
        </html>""")
