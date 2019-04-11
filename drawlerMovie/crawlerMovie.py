import socket
import ssl
import requests
from lxml import etree
from lxml import html
from time import time
import dumper
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
        print(response)
        return response
        #self.movieMapQueqe.add(link)
        
    def parse(self, url):
        response=self.fetchPage(url)
        page=response.content
        print(page)
        htmlText=etree.HTML(page, parser=etree.HTMLParser())
        #print(chardet.detect(htmlText))
        print(htmlText)
        pp = pprint.PrettyPrinter(indent=4)
        print('pprint:')
        
        pp.pprint(htmlText)
        print('end pprint:')
        if self.depth == 1:
            path="//[re:match(text(), '//a']'"
        else:
            path="//[re:match(text(), '//li|strong)']"       
        for link in htmlText.xpath(path, namespaces={"re": "http://exslt.org/regular-expressions"}):
            print(link.get('href'))
            url=link.get('href')
            if url:
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
                            if 'title' in link.attrib:
                                title=link.get('title')
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

if __name__=='__main__':
    crawlerM=CrawlerMovies()
    crawlerM.parseMainPage('https://www.loldytt.tv/')
    crawlerM.parseChildPage()
    print(crawlerM.getMovieQueue())
    print(crawlerM.getAllMovieLinks())
    #print(crawlerM.getMovieQueue())