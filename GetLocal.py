from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

import settings
import sqlite3
import json
import datetime
import random
import re
import lxml
import time

# 判断一个IP的所在地
def getCountry(ipAddress):
    try:
        response = urlopen("http://freegeoip.net/json/"+ipAddress).read().decode('utf-8')
    except HTTPError:
        return None
    except URLError:
        print("Sleeping!")
        time.sleep(settings.URLERROR_SLEEP_TIME)
        response = urlopen("http://freegeoip.net/json/"+ipAddress).read().decode('utf-8')
    responseJson = json.loads(response)
    return responseJson.get("country_code") # 返回国家代号

# 从网页中抽取出贡献者的IP
def getHistoryIPs(pageUrl):
    pageUrl = pageUrl.replace("/wiki/", "")
    historyUrl = "http://en.wikipedia.org/w/index.php?title="+pageUrl+"&action=history"
 
    print("history url:", historyUrl)
    time.sleep(settings.SLEEP_TIME)
    try:
        html = urlopen(historyUrl)
    except HTTPError:
        return None
    except URLError:
        print("Sleeping!")
        time.sleep(settings.URLERROR_SLEEP_TIME)
        html = urlopen(historyUrl)
    bsObj = BeautifulSoup(html, "lxml")
    ipAddresses = bsObj.findAll("a", {"class":"mw-anonuserlink"})
    addressList = set()
    for ipAddress in ipAddresses:
        print(ipAddress.get_text())
        addressList.add(ipAddress.get_text())
    return addressList #返回一个IP列表

# 得到所有IP的国家代号
def getIPinfo(ipList):
    IpDict = dict()
    for ipAddress in ipList:
        IpDict[ipAddress] = getCountry(ipAddress)
    return IpDict

# 储存IP信息
def storeIPinfo(objList):
    conn = sqlite3.connect("wikidata.db")
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS ipinfo (id INTEGER PRIMARY KEY AUTOINCREMENT, ip varchar(200), country varchar(200))''')
    for bsObj in objList:
        pageUrl = bsObj.attrs["href"]
        historyIPs = getHistoryIPs(pageUrl)
        IpDict = getIPinfo(historyIPs)
        for ipAddress in IpDict:
            country = IpDict[ipAddress]
            cur.execute("INSERT INTO ipinfo (ip, country) VALUES (?, ?)", (ipAddress, country))
            conn.commit()
    cur.close()
    conn.close()
            