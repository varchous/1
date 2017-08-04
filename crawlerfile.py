#! /usr/bin/env python
# -*- coding: utf-8 -*-
#import urllib2
import urllib
import urllib.request
#from urlparse import urljoin
from urllib.parse import urljoin
from urllib.parse import urlparse
#from BeautifulSoup import *
#from pysqlite2 import dbapi2 as sqlite    #################################################################################
import sqlite3
from bs4 import BeautifulSoup
import postgresql
import re
#import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')
# Создать список игнорируемых слов
ignorewords=set(['the','of','to','and','a','in','is','it'])
#import nn
#mynet=nn.searchnet('nn.db')

class crawler: # Инициализировать паука, передав ему имя базы данных
    def __init__(self,dbname):
        self.con = sqlite3.connect(dbname)

    def __del__(self):
        self.con.close()

    def dbcommit(self):
        self.con.commit()
        # Вспомогательная функция для получения идентификатора и добавления записи, если такой еще нет
    def getentryid(self,table,field,value,createnew=True):
        cur = self.con.execute(
        "select rowid from %s where %s='%s'" % (table, field, value))
        res = cur.fetchone()
        if res == None:
            cur = self.con.execute(
            "insert into %s (%s) values ('%s')" % (table, field, value))
            return cur.lastrowid
        else:
            return res[0]

    # Индексирование одной страницы
    def addtoindex(self,url,soup):
        if self.isindexed(url): return
        print ('Индексируется ' + url)

        # Получить список слов
        text = self.gettextonly(soup)
        words = self.separatewords(text)
        #print text
        # Получить идентификатор URL
        urlid = self.getentryid('urllist', 'url', url)

        # Связать каждое слово с этим URL
        for i in range(len(words)):
            word = words[i]
            if word in ignorewords: continue
            wordid = self.getentryid('wordlist', 'word', word)
            self.con.execute("insert into wordlocation(urlid,wordid,location) values (%d,%d,%d)" % (urlid, wordid, i))

        # Извлечение текста из HTML-страницы (без тегов)
    def gettextonly(self,soup):
        v = soup.string
        if v == None:
            c = soup.contents
            resulttext = ''
            for t in c:
                subtext = self.gettextonly(t)
                resulttext += subtext + '\n'
            return resulttext
        else:
            return v.strip()

 # Разбиение текста на слова
    def separatewords(self,text):
        k = [".", ",", "(", ")", "!", "?", ":", ";", "'", '"', "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-",
             "+", "=", "*", "/", "%"]
        text = text.lower()
        for i in k:
            text = text.replace(i, '')
        l = (text.split())
        #print (l)
        #splitter = re.compile(u"[^a-zа-я]")
        #return [s.lower() for s in splitter.split(text) if s != '']
        return l

 # Возвращает true, если данный URL уже проиндексирован
    def isindexed(self,url):
        u = self.con.execute ("select rowid from urllist where url='%s'" % url).fetchone()
        if u != None:
        # Проверяем, что страница посещалась
            v = self.con.execute(
            'select * from wordlocation where urlid=%d' % u[0]).fetchone()
            if v != None: return True
        return False

 # Добавление ссылки с одной страницы на другую
    def addlinkref(self,urlFrom,urlTo,linkText):
        words = self.separatewords(linkText)
        fromid = self.getentryid('urllist', 'url', urlFrom)
        toid = self.getentryid('urllist', 'url', urlTo)
        if fromid == toid: return
        cur = self.con.execute("insert into link(fromid,toid) values (%d,%d)" % (fromid, toid))
        linkid = cur.lastrowid
        for word in words:
            if word in ignorewords: continue
            wordid = self.getentryid('wordlist', 'word', word)
            self.con.execute("insert into linkwords(linkid,wordid) values (%d,%d)" % (linkid, wordid))

 # Начиная с заданного списка страниц, выполняет поиск в ширинудо заданной глубины, индексируя все встречающиеся по путистраницы
    def crawl(self,pages,depth=2):
        for i in range(depth):
            newpages=set( )
            for page in pages:
                try:
                    c=urllib.request.urlopen(page)
                except:
                    print ("Не могу открыть %s" % page)
                    continue
                soup=BeautifulSoup(c.read( ), "html.parser")
                self.addtoindex(page,soup)
                title =str(soup('title'))

                t=title[8:title.find('/')-1]
                self.con.execute("insert into title(url,title) VALUES('%s','%s')" % (page,t))

                metas = soup('meta')
                for meta in metas:
                    if('name' in dict(meta.attrs) and meta['name']=='description'):
                        c=meta['content']
                        self.con.execute("insert into description(url,description) VALUES ('%s','%s')" % (page,c))
                links=soup('a')

                #a.geturl(soup)
                imges = soup('img')
                for img in imges:
                    if ('src' in dict(img.attrs) and 'alt' in dict(img.attrs)):
                        #print(img['src'])
                        s = img['alt'].split(' ')
                        k = str(img['src'])
                        for i in range(len(s)):
                            s[i] = s[i].strip('"')
                            s[i] = s[i].lower()
                            #con = sqlite3.connect('searchindex.db')
                            #cur = con.cursor()
                            #print(k, s[i])
                            try:self.con.execute("insert into images (src, word,url) VALUES('%s','%s','%s')" % (str(k), str(s[i]),page))
                            except:continue
                            #con.commit()"""
                """imges=soup('img')
                print (imges)
                for img in  imges:
                    if ('src' in dict(img.attrs)):
                            print (img['src'])
                            destination = img['src']
                            destination='img/'+destination[destination.rfind('/'):]
                            urlimg = img['src']
                            print (destination, "(______________)", urlimg,"(_______)",img['alt'])
                            #urllib.urlretrieve(urlimg, destination)
                            """
                for link in links:
                    if ('href' in dict(link.attrs)):
                        url=urljoin(page,link['href'])
                        if url.find("'")!=-1: continue
                        url=url.split('#')[0] # удалить часть URL после знака #
                        if url[0:4]=='http' and not self.isindexed(url):
                            newpages.add(url)
                        linkText=self.gettextonly(link)
                        self.addlinkref(page,url,linkText)
                self.dbcommit( )
            pages=newpages
    def crawlvid(self,page):
        page='https://www.youtube.com/watch?v=os2HYtR186o'
        c = urllib.request.urlopen('https://www.youtube.com/watch?v=KCqabqJ1p3U')
        soup = BeautifulSoup(c.read(), "html.parser")
        metas=soup('meta')
        for meta in metas:
            if ( 'property' in dict(meta.attrs) and meta['property']=='og:video:secure_url'):
                print(meta)
                c = meta['content']
                self.con.execute("insert into vurl(url,vurl) VALUES ('%s','%s')" % (page, c))
            elif( 'property' in dict(meta.attrs) and meta['property']=='og:title'):
                print(meta)
                c = meta['content']
                self.con.execute("insert into vtitel(url,title) VALUES ('%s','%s')" % (page, c))
            elif('property' in dict(meta.attrs) and meta['property']=='og:video:tag'):
                c = meta['content']
                self.con.execute("insert into tags(url,tag) VALUES ('%s','%s')" % (page, c))
                print(meta)
        self.dbcommit()

    def createvid(self):
        self.con.execute('create table vurl(url,vurl)')
        self.con.execute('create table vtitel(url,title)')
        self.con.execute('create table stitle(url,word)')
        self.con.execute('create table tags(url,tag)')
        self.dbcommit()
    def createindextables(self):# Создание таблиц в базе данных
        self.con.execute('create table urllist(url)')
        self.con.execute('create table wordlist(word)')
        self.con.execute('create table wordlocation(urlid,wordid,location)')
        self.con.execute('create table link(fromid integer,toid integer)')
        self.con.execute('create table linkwords(wordid,linkid)')
        self.con.execute('create index wordidx on wordlist(word)')
        self.con.execute('create index urlidx on urllist(url)')
        self.con.execute('create index wordurlidx on wordlocation(wordid)')
        self.con.execute('create index urltoidx on link(toid)')
        self.con.execute('create index urlfromidx on link(fromid)')

        self.dbcommit( )
    def createdesc(self):
        self.con.execute('create table description(url,description)')
        self.con.execute('create table title(url,title)')
        self.dbcommit()

    def calculatepagerank(self, iterations=20):
        # стираем текущее содержимое таблицы PageRank
        self.con.execute('drop table if exists pagerank')
        self.con.execute('create table pagerank(urlid primary key,score)')

        # в начальный момент ранг для каждого URL равен 1
        for (urlid,) in self.con.execute('select rowid from urllist'):
            self.con.execute('insert into pagerank(urlid,score) values (%d,1.0)' % urlid)
        self.dbcommit()

        for i in range(iterations):
            print ("Iteration %d" % (i))
            for (urlid,) in self.con.execute('select rowid from urllist'):
                pr = 0.15

                # В цикле обходим все страницы, ссылающиеся на данную
                for (linker,) in self.con.execute(
                                'select distinct fromid from link where toid=%d' % urlid):
                    # Находим ранг ссылающейся страницы
                    linkingpr = self.con.execute(
                        'select score from pagerank where urlid=%d' % linker).fetchone()[0]

                    # Находим общее число ссылок на ссылающейся странице
                    linkingcount = self.con.execute(
                        'select count(*) from link where fromid=%d' % linker).fetchone()[0]
                    pr += 0.85 * (linkingpr / linkingcount)
                self.con.execute(
                    'update pagerank set score=%f where urlid=%d' % (pr, urlid))
            self.dbcommit()

class searcher:
    def __init__(self, dbname):
        self.con = sqlite3.connect(dbname)

    def __del__(self):
        self.con.close()

    def getmatchrows(self, q):
        # Строки для построения запроса
        fieldlist = 'w0.urlid'
        tablelist = ''
        clauselist = ''
        wordids = []

        # Разбить поисковый запрос на слова по пробелам
        words = q.split(' ')
        tablenumber = 0

        for word in words:
            # Получить идентификатор слова
            wordrow = self.con.execute(
            "select rowid from wordlist where word='%s'" % word).fetchone()
            if wordrow != None:
                wordid = wordrow[0]
                wordids.append(wordid)
                if tablenumber > 0:
                    tablelist += ','
                    clauselist += ' and '
                    clauselist += 'w%d.urlid=w%d.urlid and ' % (tablenumber - 1, tablenumber)
                fieldlist += ',w%d.location' % tablenumber
                tablelist += 'wordlocation w%d' % tablenumber
                clauselist += 'w%d.wordid=%d' % (tablenumber, wordid)
                tablenumber += 1

        # Создание запроса из отдельных частей
        fullquery = 'select %s from %s where %s' % (fieldlist, tablelist, clauselist)
        #print (fullquery)
        cur = self.con.cursor()
        cur.execute(fullquery)
        rows = cur.fetchall()
        #for row in rows:
        #    print (row)

        return rows, wordids

    def getscoredlist(self, rows, wordids):
        totalscores = dict([(row[0], 0) for row in rows])
        # Сюда мы позже поместим функции ранжирования
        weights =[(1.0,self.frequencyscore(rows)),(1.5,self.locationscore(rows)),(0.5,self.pagerankscore(rows)),
                  (1.0,self.inboundlinkscore(rows))
        ]#(1.0,self.nnscore(rows,wordids))]
        for (weight, scores) in weights:
            for url in totalscores:
                totalscores[url] += weight * scores[url]
        return totalscores

    def geturlname(self, id):
        return self.con.execute(
            "select url from urllist where rowid=%d" % id).fetchone()[0]

    def query(self, q):
        if (q==""):
            print("пустой")
            pass
            return
        rows, wordids = self.getmatchrows(q)
        scores = self.getscoredlist(rows, wordids)
        rankedscores = sorted([(score, url) for (url, score) in scores.items()], \
                              reverse=1)
        rows3=[]
        rows5=[]
        for (score, urlid) in rankedscores[0:len(rankedscores)]:
            print ('%f\t%s' % (score, self.geturlname(urlid)))
            rows2=self.con.execute("select title from title where url like '%s'" % self.geturlname(urlid)).fetchone()
            rows4 = self.con.execute("select description from description where url like '%s'" % self.geturlname(urlid)).fetchone()
            rows3.append(rows2)
            rows5.append(rows4)
            print(rows4,self.geturlname(urlid))
            print(rows2, self.geturlname(urlid))
        return wordids , [r[1] for r in rankedscores[0:len(rankedscores)]],rows3,rows5

    def queryimg(self, q):
        fullquery=("SELECT  DISTINCT src,url FROM images where word like '%s'" % q)
        cur = self.con.cursor()
        #cur.execute('SELECT * FROM images')
        cur.execute(fullquery)
        rows = cur.fetchall()
        print(rows)
        rows2=[]
        rows3=[]
        for i in rows:
            if i[0] not in rows2:
                rows2.append(i[0])
                rows3.append(i)
        print("",len(rows2),len(rows),len(rows3))
        for i in range(len(rows2)):
            print(rows2[i],rows3[i])
        return rows3
    def queryvid(self,q):
        print(q)
        fullquery=("SELECT DISTINCT url from tags where tag like '%s' " % q)
        cur = self.con.cursor()
        cur.execute(fullquery)
        rows5=[]
        rows4=[]
        #cur.execute('SELECT * FROM tags')
        rows = cur.fetchall()
        print(rows[0])
        for i in rows:
            fullquery2 = ("SELECT DISTINCT vurl  from vurl where url like '%s' " % i[0])
            cur = self.con.cursor()
            cur.execute(fullquery2)
            rows2 = cur.fetchall()
            rows4.append(rows2)
            print(rows2)
        for i in rows:
            fullquery3 = ("SELECT DISTINCT title  from vtitel where url like '%s' " % i[0])
            cur = self.con.cursor()
            cur.execute(fullquery3)
            rows3 = cur.fetchall()
            rows5.append(rows3)
            print(rows3)
        return rows,rows4,rows5

    def normalizescores(self, scores, smallIsBetter=0): #функция нормализации
        vsmall = 0.00001  # Предотвратить деление на нуль
        if smallIsBetter:
            minscore = min(scores.values())
            return dict([(u, float(minscore) / max(vsmall, l)) for (u, l) \
                     in scores.items()])
        else:
            maxscore = max(scores.values())
            if maxscore == 0: maxscore = vsmall
            return dict([(u, float(c) / maxscore) for (u, c) in scores.items()])

    def frequencyscore(self, rows): #метрица для подсчета частоты
        counts = dict([(row[0], 0) for row in rows])
        for row in rows: counts[row[0]] += 1
        return self.normalizescores(counts)

    def locationscore(self, rows): #метрица для определения локации
        locations = dict([(row[0], 1000000) for row in rows])
        for row in rows:
            loc = sum(row[1:])
            if loc < locations[row[0]]: locations[row[0]] = loc
        return self.normalizescores(locations, smallIsBetter=1)

    def distancescore(self, rows): #метрица для нахожденя расстояния между ключевыми словами
        # Если есть только одно слово, любой документ выигрывает!
        if len(rows[0]) <= 2: return dict([(row[0], 1.0) for row in rows])

        # Инициализировать словарь большими значениями
        mindistance = dict([(row[0], 1000000) for row in rows])
        for row in rows:
            dist = sum([abs(row[i] - row[i - 1]) for i in range(2, len(row))])
            if dist < mindistance[row[0]]: mindistance[row[0]] = dist
        return self.normalizescores(mindistance, smallIsBetter=1)

    def inboundlinkscore(self, rows): #Подсчет внешних ссылок
        uniqueurls = set([row[0] for row in rows])
        inboundcount = dict([(u, self.con.execute( \
            'select count(*) from link where toid=%d' % u).fetchone()[0]) \
                             for u in uniqueurls])
        return self.normalizescores(inboundcount)

    def pagerankscore(self, rows):
        pageranks = dict([(row[0], self.con.execute('select score from pagerank where urlid=%d' % row[0]).fetchone()[0]) for row in rows])
        maxrank = max(pageranks.values())
        normalizedscores = dict([(u, float(l) / maxrank) for (u, l) in pageranks.items()])
        return normalizedscores

    def linktextscore(self, rows, wordids):
        linkscores = dict([(row[0], 0) for row in rows])
        for wordid in wordids:
            cur = self.con.execute(
                'select link.fromid,link.toid from linkwords,link where wordid=%d and linkwords.linkid=link.rowid' % wordid)
            for (fromid, toid) in cur:
                if toid in linkscores:
                    pr = self.con.execute('select score from pagerank where urlid=%d' % fromid).fetchone()[0]
                    linkscores[toid] += pr
        maxscore = max(linkscores.values())
        normalizedscores = dict([(u, float(l) / maxscore) for (u, l) in linkscores.items()])
        return normalizedscores

    def nnscore(self, rows, wordids):
        # Получить уникальные идентификаторы URL в виде упорядоченного списка
        urlids = [urlid for urlid in set([row[0] for row in rows])]
        nnres = mynet.getresult(wordids, urlids)
        scores = dict([(urlids[i], nnres[i]) for i in range(len(urlids))])
        return self.normalizescores(scores)
class img:
    def __init__(self,dbname):
        self.con = sqlite3.connect(dbname)

    def __del__(self):
        self.con.close()

    def dbcommit(self):
        self.con.commit()
    def create(self):
        con = sqlite3.connect('searchindex.db')
        cur = con.cursor()
        cur.execute('CREATE TABLE images (src VARCHAR, word VARCHAR,url)')
        con.commit()
        """cur.execute('INSERT INTO images (src, word,url) VALUES("http://dontabak.com.ua/img/dontabakcomua-1400873765.jpg", "lol","http://dontabak.com.ua"')')
        con.commit()"""
        print (cur.lastrowid)
        #cur.execute('SELECT * FROM images')
        print (cur.fetchall())
        con.close()

    def geturl(soup):
        imges=soup('img')
        for img in  imges:
            if ('src' in dict(img.attrs)):
                    print(img['src'])
                    s=img['alt'].split(' ')
                    k = str(img['src'])
                    for i in range (len(s)):
                        s[i]=s[i].strip('"')
                        con = sqlite3.connect('searchindex.db')
                        cur = con.cursor()
                        print(k,s[i])
                        cur.execute('INSERT INTO images (src, word) VALUES("%s", "%s")' %("str(k)","str(s[i])"))
                        con.commit()
                    #destination = img['src']
                    #destination='img/'+destination[destination.rfind('/'):]
                    #urlimg = img['src']
                    #print (destination, "(______________)", urlimg,"(_______)",img['alt'])



