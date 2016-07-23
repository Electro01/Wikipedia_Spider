from urllib.request import urlopen
from bs4 import BeautifulSoup
import lxml
import sqlite3

def getAbst(articleUrl):
    html = urlopen("http://en.wikipedia.org"+articleUrl)
    bsObj = BeautifulSoup(html, "lxml")
    title = bsObj.find("h1").get_text()
    content = bsObj.find("div", {"id":"mw-content-text"}).find("p").get_text()
    print("Title:", title)   
    return (title, content)
#bsObj.find("div", {"id":"bodyContent"}).findAll("a", href=re.compile("^(/wiki/)((?!:).)*$"))

def storeAbst(link):
    conn = sqlite3.connect("wikidata.db")
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS pages (id INTEGER PRIMARY KEY AUTOINCREMENT, title varchar(200), content text)''')
    
    title, content = getAbst(link)
    cur.execute("INSERT INTO pages (title, content) VALUES (?, ?)", (title, content))
    conn.commit()

    cur.close()
    conn.close()
        