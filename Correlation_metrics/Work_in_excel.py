import openpyxl
from datetime import datetime
import sqlite3

path = '/Users/jbbaptista/Documents/Secret/Finance/ATIS Capital/Medium:Long term strategy/Correlation/'
name1 = input('Insert coin: ')
data = input('The name of file to read with .xlsx : ')

data1 = path + data

# Connect database

conn = sqlite3.connect('database.sqlite')
cur = conn.cursor()

# Create table if not exits

cur.execute(
    '''CREATE TABLE IF NOT EXISTS {} (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    time TEXT, 
    open FLOAT, 
    close FLOAT, 
    var FLOAT)'''. format(name1)
)
conn.commit()

workbook = openpyxl.load_workbook(filename=data1)
sheet = workbook.active

v1 = sheet["B"]
v2 = sheet["E"]
t1 = sheet["A"]

for i in range(1,len(v1)):
    t = t1[i].value
    time = datetime.fromtimestamp(t)

    open = v1[i].value
    close = v2[i].value

    vr = (float(close) - float(open)) / float(open) * 100
    print(time, vr)

    # Insert in database

    cur.execute(
        '''INSERT INTO {} (time, open, close, var) VALUES (?,?,?,?)'''.format(name1), (time, float(open), float(close), float(vr))
    )
    conn.commit()

conn.close()
