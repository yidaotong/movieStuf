import socket
import ssl
import requests
from lxml import etree
from lxml import html
import time
# import dumper
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
import urllib.request
import os


class Vidio:
    def __init__(self, link=b''):
        if link:
            self.rootLink == link
        else:
            self.rootLink = 'http://www.sis001.us/bbs/'
        self.asiaMovie='forum-143'
        self.movieMapQueqe = {}
        self.maxPageCount = 50
        self.downFolder='D:/github/'

    def fetchPage(self, url):
        response = requests.get(url)
        return response

    def fetchAllMoiveLink(self):
        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities['acceptSslCerts'] = True
        capabilities['acceptInsecureCerts'] = True
        chrome_options = Options()
        chrome_prefs = {}
        chrome_options.experimental_options["prefs"] = chrome_prefs
        chrome_prefs["profile.default_content_settings"] = {"images": 2}
        chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
        #chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        # chrome_options.add_argument("--proxy-server=127.0.0.1:8080")
        driver = webdriver.Chrome(options=chrome_options, desired_capabilities=capabilities)
        for i in range(1,self.maxPageCount+1):
            url=self.rootLink+self.asiaMovie+'-'+str(i)+'.html'
            #url='http://www.sis001.us/bbs/forum-143-5.html'
            print(url)
            driver.get(url)
            try:
                allsep = driver.find_elements_by_xpath(
                    '//div/div[@class="mainbox threadlist"]/form[@method="post"]/table/thead[@class="separation"]')
                for sep in allsep:
                    sepation=sep.text
                    print(sepation)
                    if sepation.strip() == '推荐主题' or sepation.strip() == '版块主题':
                        print('found')
                        #table=sep.find_element_by_xpath('..')
                        for link in sep.find_elements_by_xpath('../tbody/tr/th'):
                            print("find sepation")
                            #print(sepation.text)
                            # print(table.get_attribute("href"))
                            # em = link.find_element_by_xpath('//em')
                            emType = link.find_element_by_xpath('em/a')
                            #print(emType.text)
                            # span = link.find_element_by_xpath('//span')
                            idSpan = link.find_element_by_xpath('span')
                            if idSpan:
                                id=idSpan.get_attribute("id")
                            else:
                                id=None
                            title = link.find_element_by_xpath('span/a')
                            if title:
                                ref = title.get_attribute("href")
                            else:
                                ref=None
                            #print(title.text)
                            if emType and emType.text not in self.movieMapQueqe:
                                self.movieMapQueqe[emType.text]=[]
                            if id and title and ref:
                                self.movieMapQueqe[emType.text].append({'id':id,'title':title.text, 'link':ref})
            except:
                pass
        driver.close()
        driver.quit()

    def getAllDownloadLink(self):
        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities['acceptSslCerts'] = True
        capabilities['acceptInsecureCerts'] = True
        chrome_options = Options()
        chrome_prefs = {}
        chrome_options.experimental_options["prefs"] = chrome_prefs
        chrome_prefs["profile.default_content_settings"] = {"images": 2}
        chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
        #chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        # chrome_options.add_argument("--proxy-server=127.0.0.1:8080")
        driver = webdriver.Chrome(options=chrome_options, desired_capabilities=capabilities)
        for type in self.movieMapQueqe.keys():
            for movie in self.movieMapQueqe[type]:
                print('get downlink:')
                link=movie['link']
                print(link)
                driver.get(link)
                try:
                    for downElement in driver.find_elements_by_xpath(
                        '//div[@class="box postattachlist"]/dl/dt/a[@target="_blank"]'):
                        downLink=downElement.get_attribute('href')
                        if 'attachment' in downLink:
                            print(downLink)
                            driver.get(downLink)
                            nameElement = driver.find_element_by_xpath('//p[@class="card-header"]')
                            name = nameElement.text
                            print(name)
                            clickButton=driver.find_element_by_xpath(
                        '//div[@class="card-body"]/a[@class="btn btn-danger"]')
                            downClickLink=clickButton.get_attribute('href')
                            print(downClickLink)
                            movie['down']=[name,downClickLink]
                            #driver.get(downClickLink)
                except:
                    pass
        driver.close()
        driver.quit()

    def parse(self, url):
        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities['acceptSslCerts'] = True
        capabilities['acceptInsecureCerts'] = True
        chrome_options = Options()
        chrome_prefs = {}
        chrome_options.experimental_options["prefs"] = chrome_prefs
        chrome_prefs["profile.default_content_settings"] = {"images": 2}
        chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
        #chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        # chrome_options.add_argument("--proxy-server=127.0.0.1:8080")
        driver = webdriver.Chrome(options=chrome_options, desired_capabilities=capabilities)
        driver.get(self.rootLink)
        driver.save_screenshot('test.png')
        time.sleep(1)
        try:
            allLinks = driver.find_elements_by_xpath('//div/div[@class="mainbox threadlist"]/form/table/tbody/tr/th[@class="new"]')
            for link in allLinks:
                print(link.text)
                sepation = link.find_element_by_xpath('../../../thead[@class="separation"]')
                if sepation.text.strip()=='推荐主题' or sepation.text.strip()=='版块主题':
                    print("find sepation")
                    print(sepation.text)
                    #print(table.get_attribute("href"))
                    #em = link.find_element_by_xpath('//em')
                    emType=link.find_element_by_xpath('em/a')
                    print(emType.text)
                    #span = link.find_element_by_xpath('//span')
                    title = link.find_element_by_xpath('span/a')
                    print(title.text)
                    print(title.get_attribute("href"))


        except:
            pass
        driver.close()
        driver.quit()

    def getMovieQueue(self):
        return self.movieMapQueqe

    def downLoadAll(self):
        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities['acceptSslCerts'] = True
        capabilities['acceptInsecureCerts'] = True
        chrome_options = Options()
        chrome_prefs = {}
        chrome_options.experimental_options["prefs"] = chrome_prefs
        chrome_prefs["profile.default_content_settings"] = {"images": 2}
        chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
        #chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')

        for type in self.movieMapQueqe.keys():
            folder = self.downFolder + type
            print(folder)
            if not os.path.exists(folder):
                os.makedirs(folder)
            #downloadOptions = "download.default_directory=" + folder+'/'
            chrome_options.add_experimental_option("prefs", {
                "download.default_directory": folder,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True
            })
            #chrome_options.add_argument(downloadOptions)
            driver = webdriver.Chrome(options=chrome_options, desired_capabilities=capabilities)
            for movie in self.movieMapQueqe[type]:
                nameLink=movie['down']
                name=nameLink[0].replace('下载文件:','').strip()
                link=nameLink[1]
                print(name)
                print(link)
                if not os.path.exists(folder+'/'+name):
                    driver.get(link)
                time.sleep(2)
            time.sleep(60)
            driver.close()
            driver.quit()

if __name__=='__main__':
    t1=time.time()
    vidio=Vidio()
    vidio.fetchAllMoiveLink()
    t2 = time.time()
    t=t2-t1
    vidio.getAllDownloadLink()
    vidio.downLoadAll()
    print(vidio.getMovieQueue())
    print(t)