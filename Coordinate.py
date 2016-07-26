from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
from settings import URLERROR_SLEEP_TIME, START_PAGE, NUMBER_OF_THREADS

import GetLocal 
import GetAbstract
import random
import datetime
import re
import lxml
import threading, queue
import time

# 初始化随机数种子
random.seed(datetime.datetime.now())

# 分析网站的源码并返回内链
def getLinks(articleUrl):
    try:
        html = urlopen("http://en.wikipedia.org"+articleUrl)
    except HTTPError:
        return None
    except URLError:
        print("Sleeping!")
        time.sleep(URLERROR_SLEEP_TIME)
        html = urlopen("http://en.wikipedia.org"+articleUrl)
    bsObj = BeautifulSoup(html, "lxml")
    return bsObj.find("div", {"id":"bodyContent"}).findAll("a", href=re.compile("^(/wiki/)((?!:).)*$"))

# 设置页面
links = getLinks(START_PAGE) 
newLink = START_PAGE


# 设置缓冲队列
links_queue = queue.Queue() 

# 抓取摘要
def crawlAbs():
    global links, newLink, links_queue
    while(len(links) > 0):
        links_queue.put(newLink)
        GetAbstract.storeAbst(newLink)
        newLink = links[random.randint(0, len(links)-1)].attrs["href"]
        links = getLinks(newLink)

# 抓取IP
def crawlIP():
    global links_queue
    while True:
        linkUrl =  links_queue.get()  
        linkObj = getLinks(linkUrl)
        GetLocal.storeIPinfo(linkObj)


def run_spider(threadNum):
    global links_queue
    
    threads = []
    for i in range(threadNum):
        crawlIP_thread = threading.Thread(target = crawlIP)
        threads.append(crawlIP_thread)
    for thread in threads:
        thread.start()

    crawlAbs()
    links_queue.join()


if __name__ == '__main__':
    print("Start!\n-----------------------------")
    run_spider(NUMBER_OF_THREADS)
