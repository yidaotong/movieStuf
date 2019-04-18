import json
import codecs
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
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import optparse
import os
from datetime import datetime as dt
import operator

class CrawlerMovies:
    def __init__(self, link=b''):
        if link:
            self.rootLink==link

        else:
            self.rootLink='https://www.loldytt.tv/'
        self.movieMapQueqe={}
        self.movieMapSortedList={}
        self.depth=2
        self.doubanLink = 'https://movie.douban.com/subject_search?search_text='
        self.imdbLink='https://www.imdb.com/title/'
        self.movieStoreFile= 'movies.txt'
        self.movieWriteFile = 'movies.txt'
        self.cmdParser=None
        #self.doubanLink = 'https://movie.douban.com/'
    def fetchPage(self, url):
        header = {'content-type': 'charset=utf8'}
        try:
            response = requests.get(url, headers=header)
        except:
            print('can not open the link: '+url)
            response=None
            pass
        return response

    def parse(self, url):
        response=self.fetchPage(url)
        if response is None:
            return
        #print(response.encoding)
        response.encoding = 'GBK'
        movie=b''

        for link in Selector(response=response).xpath('//ul/li'):
            #print(link)
            urls=link.xpath('a/@href').extract()
            if urls:
                url=urls[0]
            if self.depth == 1:
                print('depth=2')
            else:
                if url:
                    pattenLink=r""+self.rootLink+"(\w+)/$"
                    pattenMovie=r""+self.rootLink+"(\w+)/(\w+)/$"
                    reLink=re.match(pattenLink,url.strip())
                    reMovie=re.match(pattenMovie,url.strip())

                    if self.depth == 1 and reLink and reLink.lastindex==1:
                        spec=reLink.group(1)
                        if spec not in self.movieMapQueqe:
                            self.movieMapQueqe[spec]={}
                    elif reMovie and reMovie.lastindex==2:
                        spec=reMovie.group(1)
                        movie=reMovie.group(2)
                        if spec not in self.movieMapQueqe:
                            self.movieMapQueqe[spec]={}
                        if movie not in self.movieMapQueqe[spec]:
                            self.movieMapQueqe[spec][movie]={}
                            self.movieMapQueqe[spec][movie]['link']=url
                            titles=link.xpath('a/@title').extract()
                            if titles:
                                self.movieMapQueqe[spec][movie]['title'] = titles[0]
                            else:
                                fullTexts=link.xpath('a/text()').extract()
                                if fullTexts:
                                    text = fullTexts[0]
                                if text:
                                    title=text
                                    self.movieMapQueqe[spec][movie]['title'] = title
                                else:
                                    self.movieMapQueqe[spec][movie]['title'] = b''
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
        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities['acceptSslCerts'] = True
        capabilities['acceptInsecureCerts'] = True
        chrome_options = Options()
        chrome_prefs = {}
        chrome_options.experimental_options["prefs"] = chrome_prefs
        chrome_prefs["profile.default_content_settings"] = {"images": 2}
        chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
        #chrome_options.add_argument('--headless')
        chrome_options.add_argument("--window-size=800,400")
        chrome_options.add_argument('--disable-gpu')
        #chrome_options.add_argument("--proxy-server=127.0.0.1:8080")
        driver = webdriver.Chrome(options=chrome_options, desired_capabilities=capabilities)
        for spec in self.movieMapQueqe.keys():
            for name in self.movieMapQueqe[spec].keys():
                movie=self.movieMapQueqe[spec][name]['title']
                det = self.movieMapQueqe[spec][name]
                if 'imdb' in self.movieMapQueqe[spec][name]['details']:
                    driver.get(self.imdbLink + self.movieMapQueqe[spec][name]['details']['imdb'])
                    try:
                        elem = driver.find_element_by_xpath(
                            '//div[@class="ratingValue"]/strong/span[@itemprop="ratingValue"]')
                        if elem:
                            rank = elem.text
                            self.movieMapQueqe[spec][name]['imdbrank'] = rank
                    except:
                        pass
                driver.get(self.doubanLink + movie)
                try:
                    elem = driver.find_element_by_xpath('//span[@class="rating_nums"]')
                    if elem:
                        rank = elem.text
                        self.movieMapQueqe[spec][name]['dbanrank'] = rank
                except:
                    pass
        driver.close()
        driver.quit()

    def getAllMoviesRank(self, movieList):
        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities['acceptSslCerts'] = True
        capabilities['acceptInsecureCerts'] = True
        chrome_options = Options()
        chrome_prefs = {}
        chrome_options.experimental_options["prefs"] = chrome_prefs
        chrome_prefs["profile.default_content_settings"] = {"images": 2}
        chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
        #chrome_options.add_argument('--headless')
        chrome_options.add_argument("--window-size=800,400")
        chrome_options.add_argument('--disable-gpu')
        #chrome_options.add_argument("--proxy-server=127.0.0.1:8080")
        driver = webdriver.Chrome(options=chrome_options, desired_capabilities=capabilities)
        for movie in movieList:
            driver.get(self.doubanLink + movie)
            elem = driver.find_element_by_xpath('//span[@class="rating_nums"]')
            rank=b''
            if elem:
                rank=elem.text
                movie['rank'] = rank
        driver.close()
        driver.quit()

    def getMovieRank(self, movieName):
        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities['acceptSslCerts'] = True
        capabilities['acceptInsecureCerts'] = True
        chrome_options = Options()
        chrome_prefs = {}
        chrome_options.experimental_options["prefs"] = chrome_prefs
        chrome_prefs["profile.default_content_settings"] = {"images": 2}
        chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
        chrome_options.add_argument('--headless')
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument('--disable-gpu')
        #chrome_options.add_argument("--proxy-server=127.0.0.1:8080")
        driver = webdriver.Chrome(options=chrome_options, desired_capabilities=capabilities)
        driver.get(self.doubanLink+movieName)
        time.sleep(300)
        driver.save_screenshot('test.png')
        searchContent=driver.find_element_by_class_name('detail')
        #print(searchContent.text)
        #print(searchContent.get_attribute('href'))
        #print(searchContent.get_attribute('name'))
        elem=driver.find_element_by_xpath('//span[@class="rating_nums"]')
        #print(elem.text)
        #driver.get(self.doubanLink + 'cry')
        #time.sleep(5)
        #href=elem.get_attribute('href')
        #print(href)
        driver.close()
        driver.quit()
        #page=self.getMovieRankPage(movieName)
        #print(page)
        #htmlText = etree.HTML(page, parser=etree.HTMLParser())
        #path='//div[@class="item-root"]'
        #print(path)
        #for link in htmlText.xpath(path):
            #print(link)

    def getMovieDetail(self, url):
        #print(url)
        response = self.fetchPage(url)
        response.encoding = 'GBK'
        downLinkMap = {}
        allDetail = {}
        nameIndex=1
        for link in Selector(response=response).xpath('//a[contains(@href,"thunder") or contains(@href,"ed2k") or contains(@href,"magnet")]'):
            if 'href' in link.attrib:
                href=link.attrib['href']
            #urls=link.xpath('a/@href').extract()
            if 'title' in link.attrib:
                title = link.attrib['title']
            if href and title:
                if title not in downLinkMap.keys():
                    downLinkMap[title] = href
                    allDetail['download'] = downLinkMap
                elif downLinkMap[title] != href:
                    newTitle=title+str(nameIndex)
                    downLinkMap[newTitle] = href
                    allDetail['download'] = downLinkMap
                    nameIndex+=1

        path='//div[@class="neirong"]/p'
        details=Selector(response=response).xpath(path)
        #print('neirong')

        #print(details[0].text)
        description = ''
        descriptionFound = False
        if details:
            #print(details[0])
            #print(details[0].text)
            de = details[0].xpath('text()')
            for text in details[0].xpath('text()').extract():
                detail=text.split(':', 1)
                if len(detail)>1:
                    if 'IMDB' in detail[0].upper():
                        allDetail['imdb'] = detail[1].strip()
                    elif '上映日期' in detail[0] or '首播' in detail[0]:
                        dateStr = detail[1]
                        reDate = re.search(r'(\d+-\d+-\d+)', dateStr)
                        if reDate:
                            allDetail['date'] = reDate.group(1)
                    elif '类' in detail[0] or '别' in detail[0]:
                        allTypes=detail[1].split('/')
                        allDetail['types'] = allTypes
                    elif '国' in detail[0] or '地' in detail[0]:
                        allDetail['area'] = detail[1]
                    else:
                        allDetail[detail[0]]=detail[1]
                elif "剧情简介" in text:
                    descriptionFound=True
                    continue
                elif '简' in text and '介' in text:
                    descriptionFound = True
                    continue
                elif '产' in text and '地' in text:
                    detail = text.strip().split('　')
                    allDetail['area'] = detail[-1]
                elif '类' in text and '别' in text:
                    detail = text.strip().split('　')
                    allTypes = detail[-1].split('/')
                    allDetail['types'] = allTypes
                elif '日期' in text:
                    detail = text.strip().split('　')
                    reDate = re.search(r'(\d+-\d+-\d+)', detail[-1])
                    if reDate:
                        allDetail['date'] = reDate.group(1)
                elif '导' in text and '演' in text:
                    detail = text.strip().split('　')
                    allDetail['导演'] = detail[-1]
                if descriptionFound:
                    description=text
            if description:
                allDetail['剧情']=description
            if 'date' not in allDetail:
                allDetail['date'] = '000-00-00'
                #print(allDetail)
        return allDetail


    def getAllMovieDetail(self):
        movieLinks=[]
        for spec in self.movieMapQueqe.keys():
            for name in self.movieMapQueqe[spec].keys():
                url=self.rootLink+spec+'/'+name+'/'
                self.movieMapQueqe[spec][name]['details']=self.getMovieDetail(url)
                if 'date' in self.movieMapQueqe[spec][name]['details']:
                    self.movieMapQueqe[spec][name]['date'] = self.movieMapQueqe[spec][name]['details']['date']
               # else:
                #    self.movieMapQueqe[spec][name]['date'] = '0'
                movieLinks.append(url)

    def saveAllMoiveToFile(self, fileName=None):
        if fileName:
            filePath=fileName
        else:
            filePath=self.movieWriteFile
        js = json.dumps(self.movieMapQueqe,ensure_ascii=False)
        with codecs.open(filePath, 'w',encoding='utf-8') as file:
            file.write(js)
            file.close()

    def getAllMoiveFromFile(self, fileName=None):
        if fileName:
            filePath=fileName
        else:
            filePath=self.movieStoreFile
        with codecs.open(filePath, 'r',encoding='utf-8') as file:
            js = file.read()
            self.movieMapQueqe = json.loads(js)
            file.close()
    def argumentsParse(self, argv):
        self.cmdParser = optparse.OptionParser()
        self.cmdParser.add_option("-f", "--file", dest="writeFile",  default="movies.txt",
                          help="write movie info to FILE", metavar="FILE")
        self.cmdParser.add_option("-r", "--read", dest="readFile",
                          help="read movie info from File", metavar="FILE")
        self.cmdParser.add_option("-s", "--search", dest="search",
                          help="search movies list split by ,")
        self.cmdParser.add_option("-a", "--rank", dest="rank",
                          help="search movies lowest rank")
        self.cmdParser.add_option("-d", "--date", dest="dateSince",
                          help="list movies since the date given, e.g 2018-01-09")
        self.cmdParser.add_option("-n", "--newest", dest="newest",default="10",
                          help="list the newest movies account given, e.g 20")
        (options, args) = self.cmdParser.parse_args(sys.argv)
        return options

    def getMovieDetailByList(self, movies):
        account = 0
        for movie in movies:
            for spec in self.movieMapQueqe:
                for m in self.movieMapQueqe[spec]:
                    if 'title' in self.movieMapQueqe[spec][m]:
                        if movie in self.movieMapQueqe[spec][m]['title']:
                            print(self.movieMapQueqe[spec][m])
                            self.printMovieDetail(self.movieMapQueqe[spec][m])
                            account += 1
        print(account)

    def getMovieDetailByRank(self, rank):
        account=0
        for spec in self.movieMapQueqe:
            for m in self.movieMapQueqe[spec]:
                if 'dbanrank' in self.movieMapQueqe[spec][m]:
                    if float(rank) <= float(self.movieMapQueqe[spec][m]['dbanrank']):
                        self.printMovieDetail(self.movieMapQueqe[spec][m])
                        account += 1
        print(account)

    def printMovieDetail(self, movieMap):
        if 'title' in movieMap:
            print(movieMap['title'] + ':')
            for item in movieMap:
                if item != 'title':
                    if item == 'details':
                        print('下载链接：')
                        if 'download' in movieMap['details']:
                            for link in movieMap['details']['download']:
                                print('\t'+link+':'+movieMap['details']['download'][link])
                        if 'area' in movieMap['details']:
                                print('产地：' + movieMap['details']['area'])
                        if '剧情' in movieMap['details']:
                            print('剧情： '+ movieMap['details']['剧情'])

                    elif item == 'dbanrank':
                        print('豆瓣评分' + ':' + movieMap[item])
                    elif item == 'types':
                        print('类型：'+'/'.join(movieMap['details']['types']))
        else:
            print('not title found')

    def createMovieListByDate(self):
        self.movieMapSortedList={}
        movieDateMap = {}
        for spec in self.movieMapQueqe:
            if spec not in self.movieMapSortedList:
                movieDateMap[spec]={}
                self.movieMapSortedList[spec]=[]
            for m in self.movieMapQueqe[spec]:
                if 'date' in self.movieMapQueqe[spec][m]['details']:
                    movieDateMap[spec][m] = self.movieMapQueqe[spec][m]['details']['date']
        print(movieDateMap)
        for spec in movieDateMap:
            sortedMovies=sorted(movieDateMap[spec].items(), reverse=True, key=operator.itemgetter(1))
            sortedKeys=c=[x[0] for x in sortedMovies]
            print(sortedKeys)
            self.movieMapSortedList[spec]=[]
            for movieKey in sortedKeys:
                self.movieMapSortedList[spec].append(self.movieMapQueqe[spec][movieKey])

    def printMoviesSinceDate(self, dateStr):
        for spec in self.movieMapSortedList:
            for moive in self.movieMapSortedList[spec]:
                if 'date' in moive['details']:
                    movieDate = dt.strptime(moive['details']['date'], '%Y-%m-%d')
                    if movieDate > dt.strptime(dateStr, '%Y-%m-%d'):
                        self.printMovieDetail(moive)

    def printMoviesNest(self, count):
        js = json.dumps(self.movieMapSortedList, ensure_ascii=False)
        with codecs.open('newestcount.txt', 'w', encoding='utf-8') as file:
            file.write(js)
            file.close()
        for spec in self.movieMapSortedList:
            for index in range(0,int(count)-1):
                self.printMovieDetail(self.movieMapSortedList[spec][index])



if __name__=='__main__':

    t1=time.time()
    crawlerM=CrawlerMovies()
    options = crawlerM.argumentsParse(sys.argv)
    if options.writeFile and not options.readFile:
        crawlerM.parseMainPage('https://www.loldytt.tv/')
        crawlerM.parseChildPage()
        crawlerM.getAllMovieDetail()
        crawlerM.parseMoviesRank()
        crawlerM.saveAllMoiveToFile(options.writeFile)
    if options.readFile:
        if os.path.exists(options.readFile):
            crawlerM.getAllMoiveFromFile(options.readFile)
        else:
            crawlerM.getAllMoiveFromFile()
            print(crawlerM.getMovieDetail('https://www.loldytt.tv/Dongzuodianying/LLDRM/'))
            print(crawlerM.getMovieDetail('https://www.loldytt.tv/Dongzuodianying/XBYZ/'))
    crawlerM.createMovieListByDate()

    if options.search:
        movies = options.search.split(':')
        print(movies)
        crawlerM.getMovieDetailByList(movies)

    if options.rank:
        print(options.rank)
        crawlerM.getMovieDetailByRank(options.rank)

    if options.dateSince:
        print(options.dateSince)
        crawlerM.printMoviesSinceDate(options.dateSince)

    if options.newest:
        crawlerM.printMoviesNest(options.newest)

    #print(crawlerM.getMovieDetail('https://www.loldytt.tv/Xijudianying/FCRS/'))
    t2 = time.time()
    t=t2-t1
    #print(crawlerM.getMovieQueue())
    print(t)
    print('get all')
    crawlerN = CrawlerMovies()


    crawlerN.getAllMoiveFromFile()
    #crawlerN.saveAllMoiveToFile('newmovie.txt')
    #print(crawlerM.getMovieQueue())