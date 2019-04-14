import socket
import ssl
import requests
from lxml import etree
from lxml import html
import time
#import dumper
import pprint
import unicodedata
import chardet
import sys
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import DesiredCapabilities



class CrawlerMovies:
    def __init__(self, link=b''):
        if link:
            self.rootLink==link

        else:
            self.rootLink='https://www.loldytt.tv/'
        self.movieMapQueqe={}
        self.depth=1
        self.doubanLink = 'https://movie.douban.com/subject_search?search_text='
        #self.doubanLink = 'https://movie.douban.com/'
    def fetchPage(self, url):
        #sock = ssl.wrap_socket(socket.socket())
        #sock=socket.socket()
        response = requests.get(url)
        #print('return')
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
            #print(link)
            url=link.get('href')
            #print(url)
            #if self.depth == 1:
                #print('depth=2')
            if url:
                #print(link.get('href'))
                pattenLink=r""+self.rootLink+"(\w+)/$"
                pattenMovie=r""+self.rootLink+"(\w+)/(\w+)/$"
                #print(pattenLink)
                #print(pattenMovie)
                reLink=re.match(pattenLink,url.strip())
                reMovie=re.match(pattenMovie,url.strip())
                #print(reMovie)
                
                if self.depth == 1 and reLink and reLink.lastindex==1:
                    #print(reLink.group(1))
                    spec=reLink.group(1)
                    if spec not in self.movieMapQueqe:
                        self.movieMapQueqe[spec]={}
                elif reMovie and reMovie.lastindex==2:
                    #print("movie link found")
                    #print (reMovie.group(0))
                    #print(reMovie.group(1))
                    #print(reMovie.group(2))
                    spec=reMovie.group(1)
                    movie=reMovie.group(2)
                    if spec not in self.movieMapQueqe:
                        self.movieMapQueqe[spec]={}
                    else:
                        if movie not in self.movieMapQueqe[spec]:
                            title=link.get('title')
                            if title:
                                self.movieMapQueqe[spec][movie] = {'title': title}
                            else:
                                fullText=link.xpath('text()')
                                if fullText:
                                    text = fullText[0]
                                if text:
                                    title=text
                                    #print('title found')
                                    #print(title)
                                    self.movieMapQueqe[spec][movie] = {'title': title}
                                else:
                                    #print('not title, get attrib')
                                    #print(link.attrib)
                                    self.movieMapQueqe[spec][movie] = {'title': b''}
                        #elif not self.movieMapQueqe[spec][movie]:
                            #self.movieMapQueqe[spec][movie]=b''
        return b''
    
    def parseMainPage(self, url):
        self.parse(url)
        self.depth += 1
    def parseChildPage(self):
        for spec in self.movieMapQueqe.keys():
            #if spec == 'Zuixinriju':
             #   print('zuixinriju')
            url=self.rootLink+spec
            #print("get child url")
            #print(url)
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
        #print(searchLink)
        response = requests.get(searchLink)
        return response.content

    def parseMoviesRank(self):
        driver = webdriver.Firefox(service_log_path='./geckodriver.log')
        for spec in self.movieMapQueqe.keys():
            for name in self.movieMapQueqe[spec].keys():
                movie=self.movieMapQueqe[spec][name]['title']
                driver.get(self.doubanLink + movie)
                rank = b''
                try:
                    rank = driver.find_element_by_xpath('//span[@class="rating_nums"]').text
                except:
                    #print('\nNo rank for movie:' + movie)
                    pass
                self.movieMapQueqe[spec][name]['rank'] = rank
        driver.close()
        driver.quit()

    def getAllMoviesRank(self, movieList):
        driver = webdriver.Firefox(service_log_path='./geckodriver.log')
        for movie in movieList:
            driver.get(self.doubanLink + movie)
            elem = driver.find_element_by_xpath('//span[@class="rating_nums"]')
            rank=b''
            if elem:
                rank=elem.text
        driver.close()
        driver.quit()

    def getMovieRank(self, movieName):
        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities['acceptSslCerts'] = True
        capabilities['acceptInsecureCerts'] = True
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        #chrome_options.add_argument("--proxy-server=127.0.0.1:8080")
        driver = webdriver.Chrome(options=chrome_options, desired_capabilities=capabilities)
        driver.get(self.doubanLink+movieName)
        driver.save_screenshot('test.png')
        time.sleep(5)
        searchContent=driver.find_element_by_class_name('detail')
        #print(searchContent.text)
        #print(searchContent.get_attribute('href'))
        #print(searchContent.get_attribute('name'))
        elem=driver.find_element_by_xpath('//span[@class="rating_nums"]')
        #print(elem.text)
        driver.get(self.doubanLink + 'cry')
        time.sleep(5)
        #href=elem.get_attribute('href')
        #print(href)
        driver.close()
        driver.quit()
        page=self.getMovieRankPage(movieName)
        #print(page)
        htmlText = etree.HTML(page, parser=etree.HTMLParser())
        path='//div[@class="item-root"]'
        #print(path)
        #for link in htmlText.xpath(path):
            #print(link)

    def getMovieDetail(self, url):
        print(url)
        response = self.fetchPage(url)
        page = response.content
        print(page)
        htmlText = etree.HTML(page, parser=etree.HTMLParser())
        path = '//ul[@class="downurl"]/li/a'
        allDetail={}
        downLinkMap={}
        for link in htmlText.xpath(path):
            #print(link)
            #print(link.get('href'))
            #print(link.get('title'))
            href=link.get('href')
            title=link.get('title')
            downLinkMap[title]=href
            #return downLinkMap
        if downLinkMap:
            allDetail['download']=downLinkMap
        path='//div[@class="neirong"]/p'
        details=htmlText.xpath(path)
        #print('neirong')

        #print(details[0].text)
        description = ''
        descriptionFound = False
        if details:
            print(details[0])
            print(details[0].text)
            if details[0].text:
                detail=details[0].text.split(':',1)
                if len(detail)>1:
                    allDetail[detail[0]]=detail[1]
                else:
                    description=details[0].text

            for br in htmlText.xpath('//div[@class="neirong"]/p/br'):
                #print(br.tail)
                if br and br.tail:
                    print (br)
                    print(br.attrib)
                    if "剧情简介" in br.tail:
                        descriptionFound=True
                    elif descriptionFound:
                        description=description+br.tail
                    else:
                        detail = br.tail.split(':', 1)
                        if len(detail) > 1:
                            allDetail[detail[0]] = detail[1]
            if description:
                allDetail['剧情']=description
                #print(allDetail)
        return allDetail


    def getAllMovieDetail(self):
        movieLinks=[]
        for spec in self.movieMapQueqe.keys():
            for name in self.movieMapQueqe[spec].keys():
                url=self.rootLink+spec+'/'+name+'/'
                self.movieMapQueqe[spec][name]['details']=self.getMovieDetail(url)
                movieLinks.append(url)

if __name__=='__main__':
    t1=time.time()
    crawlerM=CrawlerMovies()
    #crawlerM.parseMainPage('https://www.loldytt.tv/')
    #crawlerM.parseChildPage()
    #crawlerM.parseMoviesRank()
    #crawlerM.getAllMovieDetail()

    #print(crawlerM.getAllMovieLinks())
    keywords = {
        'search_text': '九品芝麻官',
        
    }

    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 \
               (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'}
    #print(crawlerM.getMovieQueue())
    html_post = requests.post(crawlerM.doubanLink, data=keywords)
    print(html_post.content)
    ret=crawlerM.getMovieRank('九品芝麻官')
    print(ret)
    #crawlerM.getMovieDetail('https://www.loldytt.tv/Juqingdianying/HYLDMWZ/')
    t2 = time.time()
    t=t2-t1
    #print(crawlerM.getMovieQueue())
    print(t)