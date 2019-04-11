import socket
import ssl
import requests
from lxml import etree
from lxml import html
from time import time
#import dumper
import pprint
import unicodedata
import chardet
import sys
import re

class CrawlerMovies:
    def __init__(self, link=b''):
        if link:
            self.rootLink==link

        else:
            self.rootLink='https://www.loldytt.tv/'
        self.movieMapQueqe={}
        self.depth=1
        self.doubanLink = 'https://movie.douban.com/subject_search?search_text='
    def fetchPage(self, url):
        #sock = ssl.wrap_socket(socket.socket())
        #sock=socket.socket()
        response = requests.get(url)
        print('return')
        #request = 'GET {} HTTP/1.0\r\nHost:www.loldytt.tv\r\n\r\n'.format(url)
        #response=b''
        #chunk=sock.recv(4096)
        #while chunk:
            #response += chunk
            #chunk=sock.recv(4096)
        #link = self.parseLink(response)
        #print(response)
        return response
        #self.movieMapQueqe.add(link)
        
    def parse(self, url):
        response=self.fetchPage(url)
        page=response.content
        #print(page)
        htmlText=etree.HTML(page, parser=etree.HTMLParser())
        #print(chardet.detect(htmlText))
        #print(htmlText)
        #pp = pprint.PrettyPrinter(indent=4)
        #print('pprint:')
        
        #pp.pprint(htmlText)
        #print('end pprint:')

        path='//a'
        for link in htmlText.xpath(path):
            print(link)
            url=link.get('href')
            print(url)
            if self.depth == 1:
                print('depth=2')
            if url:
                print(link.get('href'))
                pattenLink=r""+self.rootLink+"(\w+)/$"
                pattenMovie=r""+self.rootLink+"(\w+)/(\w+)/$"
                print(pattenLink)
                print(pattenMovie)
                reLink=re.match(pattenLink,url.strip())
                reMovie=re.match(pattenMovie,url.strip())
                print(reMovie)
                
                if self.depth == 1 and reLink and reLink.lastindex==1:
                    print(reLink.group(1))
                    spec=reLink.group(1)
                    if spec not in self.movieMapQueqe:
                        self.movieMapQueqe[spec]={}
                elif reMovie and reMovie.lastindex==2:
                    print("movie link found")
                    print (reMovie.group(0))
                    print(reMovie.group(1))
                    print(reMovie.group(2))
                    spec=reMovie.group(1)
                    movie=reMovie.group(2)
                    if spec not in self.movieMapQueqe:
                        self.movieMapQueqe[spec]={}
                    else:
                        if movie not in self.movieMapQueqe[spec]:
                            title=link.get('title')
                            if title:
                                self.movieMapQueqe[spec][movie] = title
                            else:
                                fullText=link.xpath('text()')
                                if fullText:
                                    text = fullText[0]
                                if text:
                                    title=text
                                    print('title found')
                                    print(title)
                                    self.movieMapQueqe[spec][movie]=title
                                else:
                                    print('not title, get attrib')
                                    print(link.attrib)
                                    self.movieMapQueqe[spec][movie]=b''
                        #elif not self.movieMapQueqe[spec][movie]:
                            #self.movieMapQueqe[spec][movie]=b''
        return b''
    
    def parseMainPage(self, url):
        self.parse(url)
        self.depth += 1
    def parseChildPage(self):
        for spec in self.movieMapQueqe.keys():
            if spec == 'Zuixinriju':
                print('zuixinriju')
            url=self.rootLink+spec
            print("get child url")
            print(url)
            self.parse(url)
    def getMovieQueue(self):
        return self.movieMapQueqe
    def getAllMovieLinks(self):
        movieLinks=[]
        for spec in self.movieMapQueqe.keys():
            for name in self.movieMapQueqe[spec].keys():
                url=self.rootLink+spec+'/'+name+'/'
                movieLinks.append(url)
        return movieLinks
    def getMovieRankPage(self,movieName):
        searchLink=self.doubanLink+movieName
        print(searchLink)
        response = requests.get(searchLink)
        return response.content
    def getMovieRank(self, movieName):
        page=self.getMovieRankPage(movieName)
        print(page)
        htmlText = etree.HTML(page, parser=etree.HTMLParser())
        path='//div[@class="item-root"]'
        print(path)
        for link in htmlText.xpath(path):
            print(link)

if __name__=='__main__':
    crawlerM=CrawlerMovies()
    crawlerM.parseMainPage('https://www.loldytt.tv/')
    crawlerM.parseChildPage()
    print(crawlerM.getMovieQueue())
    print(crawlerM.getAllMovieLinks())
    keywords = {
        'search_text': '九品芝麻官',
    }

    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 \
               (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'}
    #print(crawlerM.getMovieQueue())
    html_post = requests.post(crawlerM.doubanLink, data=keywords)
    print(html_post)
    ret=crawlerM.getMovieRank('九品芝麻官')
    print(ret)