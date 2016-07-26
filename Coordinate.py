from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

import settings
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
        time.sleep(settings.URLERROR_SLEEP_TIME)
        html = urlopen("http://en.wikipedia.org"+articleUrl)
    bsObj = BeautifulSoup(html, "lxml")
    return bsObj.find("div", {"id":"bodyContent"}).findAll("a", href=re.compile("^(/wiki/)((?!:).)*$"))

# 设置起始页面
links = getLinks(settings.START_PAGE) 
newLink = settings.START_PAGE


# 设置缓冲队列
links_queue = queue.Queue(50000) 

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

#运行
def run_spider():
    global links_queue
    # 设置一个线程用来抓取摘要和Link
    crawlAbs_thread = threading.Thread(target = crawlAbs)
    crawlAbs_thread.start()
    # 第二个线程用来从队列中提取Link并抓取
    crawlIP()

    links_queue.join()

def run_test():
    global links_queue
    
    threads = []
    for i in range(settings.NUMBER_OF_THREADS):
        crawlIP_thread = threading.Thread(target = crawlIP)
        threads.append(crawlIP_thread)
    
    for thread in threads:
        thread.start()
    crawlAbs()

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    print("Start!\n-----------------------------")
    run_test()
    #run_spider()
