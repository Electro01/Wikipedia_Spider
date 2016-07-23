from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

import sqlite3
import json
import datetime
import random
import re
import lxml

def getCountry(ipAddress):
    try:
        response = urlopen("http://freegeoip.net/json/"+ipAddress).read().decode('utf-8')
    except HTTPError:
        return None
    responseJson = json.loads(response)
    return responseJson.get("country_code")


def getHistoryIPs(pageUrl):
    pageUrl = pageUrl.replace("/wiki/", "")
    historyUrl = "http://en.wikipedia.org/w/index.php?title="+pageUrl+"&action=history"
 
    print("history url:", historyUrl)
    html = urlopen(historyUrl)
    #bsObj = BeautifulSoup(html, "html.parser")
    bsObj = BeautifulSoup(html, "lxml")
    ipAddresses = bsObj.findAll("a", {"class":"mw-anonuserlink"})
    addressList = set()
    for ipAddress in ipAddresses:
        print(ipAddress)
        addressList.add(ipAddress.get_text())
    return addressList #返回一个IP列表


def getIPinfo(ipList):
    IpDict = dict()
    for ipAddress in ipList:
        IpDict[ipAddress] = getCountry(ipAddress)
    return IpDict

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
            