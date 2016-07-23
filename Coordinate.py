from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

import GetLocal 
import GetAbstract
import random
import datetime
import re
import lxml
import threading, queue

# 初始化随机数种子
random.seed(datetime.datetime.now())

def getLinks(articleUrl):
    try:
        html = urlopen("http://en.wikipedia.org"+articleUrl)
    except HTTPError:
        return None
    bsObj = BeautifulSoup(html, "lxml")
    return bsObj.find("div", {"id":"bodyContent"}).findAll("a", href=re.compile("^(/wiki/)((?!:).)*$"))

# 设置起始页面
links = getLinks("/wiki/Kevin_Bacon") 
newLink = '/wiki/Kevin_Bacon'


# 设置缓冲队列
links_queue = queue.Queue(50000)


def crawlAbs():
    global links, newLink, links_queue
    while(len(links) > 0):
        GetAbstract.storeAbst(newLink)
        links_queue.put(newLink)
        #GetLocal.storeIPinfo(links)
        newLink = links[random.randint(0, len(links)-1)].attrs["href"]
        links = getLinks(newLink)

def crawlIP():
    global links_queue
    while True:
        linkUrl = links_queue.get()
        linkObj = getLinks(linkUrl)
        GetLocal.storeIPinfo(linkObj)

def run():
    global links_queue
    print("Start!")
    crawlAbs_thread = threading.Thread(target = crawlAbs)
    crawlIP_thread = threading.Thread(target = crawlIP)
    crawlAbs_thread.start()
    crawlIP_thread.start()
    links_queue.join()



if __name__ == '__main__':
    #run()
    links_queue.put('Kevin_Bacon')
    links_queue.put('Ed Harris')
    crawlIP()
    #crawlAbs()