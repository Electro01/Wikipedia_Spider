import sqlite3

class DataStorage(object):
    conn = None
    cur = None
    def __init__(self):
        pass
    def storeSqlite(self):
        pass
    def storeTxt(self):
        pass

    @staticmethod
    def initSqlite():
        pass
    @staticmethod
    def delSqlite():
        pass

class IpData(DataStorage):

    def __init__(self, ip, country):
        self.ipAddress = ip
        self.country = country
    
    def storeSqlite(self):
        IpData.cur.execute("INSERT INTO ipinfo (ip, country) VALUES (?, ?)", (self.ipAddress, self.country))
        IpData.conn.commit()
    
    def storeTxt(self):
        with open("ip.txt","a+") as file:
            file.write(self.ipAddress + ' ' + self.country + '\n')
    
    @staticmethod
    def initSqlite():
        IpData.conn = sqlite3.connect("IP.db")
        IpData.cur = IpData.conn.cursor()
        IpData.cur.execute('''CREATE TABLE IF NOT EXISTS ipinfo (id INTEGER PRIMARY KEY AUTOINCREMENT, ip varchar(200), country varchar(200))''')

    @staticmethod
    def delSqlite():
        IpData.cur.close()
        IpData.conn.close()
        

class UrlData(DataStorage):

    def __init__(self, historyUrl):
        self.historyUrl = historyUrl

    def storeSqlite(self):
        UrlData.cur.execute("INSERT INTO history (url) VALUES (?)", (self.historyUrl,))
        UrlData.conn.commit()
    
    def storeTxt(self):
        with open("ip.txt","a+") as file:
            file.write(self.historyUrl + '\n')
    
    @staticmethod
    def initSqlite():
        UrlData.conn = sqlite3.connect("IP.db")
        UrlData.cur = UrlData.conn.cursor()
        UrlData.cur.execute('''CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY AUTOINCREMENT, url varchar(200))''')

    @staticmethod
    def delSqlite():
        UrlData.cur.close()
        UrlData.conn.close()

    


