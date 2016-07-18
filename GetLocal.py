from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import json
import datetime
import random
import re
#import lxml

def getCountry(ipAddress):
    try:
        response = urlopen("http://freegeoip.net/json/"+ipAddress).read().decode('utf-8')
    except HTTPError:
        return None
    responseJson = json.loads(response)
    return responseJson.get("country_code")
#print(getCountry("119.180.157.203"))

def getLinks(articleUrl):
    html = urlopen("http://en.wikipedia.org"+articleUrl)
    bsObj = BeautifulSoup(html, "html.parser")
    return bsObj.find("div", {"id":"bodyContent"}).findAll("a", href=re.compile("^(/wiki/)((?!:).)*$"))


def getHistoryIPs(pageUrl):
    pageUrl = pageUrl.replace("/wiki/", "")
    historyUrl = "http://en.wikipedia.org/w/index.php?title="+pageUrl+"&action=history"
    print("history url is: "+historyUrl)
    html = urlopen(historyUrl)
    bsObj = BeautifulSoup(html, "html.parser")
    #finds only the links with class "mw-anonuserlink" which has IP addresses instead of usernames
    ipAddresses = bsObj.findAll("a", {"class":"mw-anonuserlink"})
    addressList = set()
    for ipAddress in ipAddresses:
        addressList.add(ipAddress.get_text())
    return addressList

links = getLinks("/wiki/Python_(programming_language)")

if __name__ == '__main__':
    print("start!")
    while(len(links) > 0):
        for link in links:
            print("-------------------") 
            historyIPs = getHistoryIPs(link.attrs["href"])
            for historyIP in historyIPs:
                country = getCountry(historyIP)
                if country is not None:
                    with open("IP.txt", 'a+') as file:
                        file.write(historyIP + '\n')
                    print(historyIP+" is from "+country)

        newLink = links[random.randint(0, len(links)-1)].attrs["href"]
        links = getLinks(newLink)