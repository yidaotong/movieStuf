import requests
from scrapy.selector import Selector
import time
import random
import scrapy

urlList=['https://www.loldytt.tv/Dongzuodianying/LLDRM/', 'https://www.loldytt.tv/Dongzuodianying/XBYZ/', 'https://www.loldytt.tv/Xijudianying/FCRS/']
#global readCount = 0

def fetch(url):
    header = {'content-type': 'charset=utf8'}
    try:
        scrapy.Request(url, callback=parse_links)
    except:
        print('can not open the link: ' + url)
        pass

def fetchAll(urlList):
    linkList=[]
    for url in urlList:
        linkList.append(fetch(url))
    return linkList

def parse_links(response):
    for link in Selector(response=response).xpath('//ul/li'):
        urls = link.xpath('a/@href').extract()
        return urls

def asycGen():
    yield 1
    print('gen yield 1')
    yield 2
    print('gen yield 3')
    return 'gen exit'

def readSimulate():
    t = random.randint(2,6)
    time.sleep(t)
    yield t
    readCount += 1
    print("read:" + str(readCount))
    return t

def parseRead(t):
    print(t)

def readAllSimulate():
    tList=[]
    rea = readSimulate()
    for i in range(1,5):
        yield from readSimulate()