import numpy as np
import matplotlib.pyplot as plt

import sqlite3

conn = sqlite3.connect("IP.db")
cur = conn.cursor()
datas = cur.execute("SELECT * FROM ipinfo")
datasList = list(datas)
countrySet = set()
for data in datasList:
    countrySet.add(data[2])

dataDict = dict()
for i in countrySet:
    dataDict[i] = 0

for data in datasList:
    dataDict[data[2]] += 1

countryMeans = []
numMeans = []
for i in dataDict:
    countryMeans.append(i)
    numMeans.append(dataDict[i])

print(countryMeans)
print(numMeans)

