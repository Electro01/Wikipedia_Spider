import sqlite3


class IpData(object):
    conn = None
    cur = None
    def __init__(self, ip, country):
        self.ipAddress = ip
        self.country = country
    
    def storeSqlite(self):
        print("正在写入")
        IpData.cur.execute("INSERT INTO ipinfo (ip, country) VALUES (?, ?)", (self.ipAddress, self.country))
        IpData.conn.commit()
    
    '''def storeTxt(self):
        with open("ip.txt","a+") as file:
            file.write(self.ipAddress + ' ' + self.country + '\n')'''
    
    @staticmethod
    def initSqlite():
        #global conn, cur
        IpData.conn = sqlite3.connect("IP.db")
        IpData.cur = IpData.conn.cursor()
        IpData.cur.execute('''CREATE TABLE ipinfo (id INTEGER PRIMARY KEY AUTOINCREMENT, ip varchar(200), country varchar(200))''')

    @staticmethod
    def delSqlite():
        IpData.cur.close()
        IpData.conn.close()
        

IpData.initSqlite()
a = IpData('12123','US')
b = IpData('12123d','U2S')
a.storeSqlite()
b.storeSqlite()
IpData.delSqlite()
print("SUCCESS")


