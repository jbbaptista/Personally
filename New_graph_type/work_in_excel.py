import openpyxl
from datetime import datetime
import sqlite3

path = '/Users/jbbaptista/Documents/Secret/Finance/ATIS Capital/New chart type/Excel data/'

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
    high FLOAT, 
    low FLOAT,
    close FLOAT, 
    volume FLOAT)'''. format(name1)
)
conn.commit()

workbook = openpyxl.load_workbook(filename=data1)
sheet = workbook.active

'''
INFORMATION VALUES 
v1 -> open ; v2 -> close ; v3 -> high ; v4 ->low 
'''

v1 = sheet["B"]
v2 = sheet["E"]
v3 = sheet["C"]
v4 = sheet["D"]
v5 = sheet["F"]

t1 = sheet["A"]

for i in range(1,len(v1)):
    t = t1[i].value
    time = datetime.fromtimestamp(t)

    open = v1[i].value
    close = v2[i].value
    high = v3[i].value
    low = v4[i].value

    volume = v5[i].value

    # Insert in database

    cur.execute(
        '''INSERT INTO {} (time, open, high, low, close, volume) VALUES (?,?,?,?,?,?)'''.format(name1), (time, float(open), float(high), float(low), float(close), float(volume))
    )
    conn.commit()

conn.close()
