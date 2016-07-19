import sqlite3

def showIpData():
    conn = sqlite3.connect("IP.db")
    cur = conn.cursor()
    List = cur.execute("SELECT * FROM ipinfo")
    print(List.fetchall())
    cur.close()
    conn.close()


if __name__ == '__main__':
    showIpData()