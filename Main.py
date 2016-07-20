import DataStorage
from GetLocal import *


# 设置起始页面
links = getLinks("/wiki/Unix") 

def main():
    global links
    print("start!")
    DataStorage.IpData.initSqlite()
    while(len(links) > 0):
        for link in links:
            print("-------------------------------") 
            historyIPs = getHistoryIPs(link.attrs["href"])
            for historyIP in historyIPs:
                country = getCountry(historyIP)
                if country is not None:
                    try:
                        user = DataStorage.IpData(historyIP, country)
                        user.storeSqlite()
                    except:
                        DataStorage.IpData.delSqlite()
                        exit()
                    print(historyIP+" is from "+country)

        newLink = links[random.randint(0, len(links)-1)].attrs["href"]
        links = getLinks(newLink)
    DataStorage.IpData.delSqlite()


if __name__ == '__main__':
    main()


