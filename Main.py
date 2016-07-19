
# 设置起始页面
links = getLinks("/wiki/Python_(programming_language)") 

def main():
    print("start!")
    while(len(links) > 0):
        for link in links:
            print("-------------------------------") 
            historyIPs = getHistoryIPs(link.attrs["href"])
            for historyIP in historyIPs:
                country = getCountry(historyIP)
                if country is not None:
                    with open("IP.txt", 'a+') as file:
                        file.write(historyIP + ' ' + country + '\n')
                    print(historyIP+" is from "+country)

        newLink = links[random.randint(0, len(links)-1)].attrs["href"]
        links = getLinks(newLink)


if __name__ == '__main__':
    main()


