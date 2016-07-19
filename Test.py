import sqlite3

def showIpData():
    conn = sqlite3.connect("IP.db")
    cur = conn.cursor()
    List = cur.execute("SELECT * FROM ipinfo")
    print(List.fetchall())
    cur.close()
    conn.close()

class base():
    count = 0
    def __init__(self):
        base.count += 1
    @staticmethod
    def tes():
        base.count+=10
    @staticmethod
    def printf():
        print(base.count)

if __name__ == '__main__':
    showIpData()
    print('----------------------')
    a = base()
    base.printf()
    b = base()
    base.printf()
    base.tes()
    base.printf()
