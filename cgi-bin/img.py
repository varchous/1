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
#text2 = form.getfirst("TEXT_2", "не задано")
text1 = html.escape(text1)
#text2 = html.escape(text2)
e=crawlerfile.searcher('searchindex.db')
print("Content-type: text/html\n")
print("""<!DOCTYPE HTML>
<html>
<head>
<meta charset="utf-8">
<title>Обработка данных форм</title>
</head>
<body>
    <form action="/cgi-bin/imgquery.py">
	Enter query
        <input type="text" name="TEXT_1">
        <input type="submit">
    </form>
</body>
</html>""")


