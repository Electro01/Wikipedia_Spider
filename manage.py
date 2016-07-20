import sqlite3

def showIpData():
    conn = sqlite3.connect("IP.db")
    cur = conn.cursor()
    List = cur.execute("SELECT * FROM ipinfo")
    for data in List.fetchall():
        print(data)
    cur.close()
    conn.close()

def showDataNum():
    conn = sqlite3.connect("IP.db")
    cur = conn.cursor()
    maxID = cur.execute("SELECT max(id) FROM ipinfo")
    ipNum = list(maxID)[0][0]
    maxID = cur.execute("SELECT max(id) FROM history")
    urlNum = list(maxID)[0][0]

    print("The amount of URL data:",urlNum)
    print("The amount of IP data:",ipNum)
    



def DataStoragetest():
    IpData.initSqlite()
    a = IpData('12123','US')
    b = IpData('12123d','U2S')
    a.storeSqlite()
    b.storeSqlite()
    IpData.delSqlite()
    print("SUCCESS")



if __name__ == '__main__':
    #showIpData()
    showDataNum()