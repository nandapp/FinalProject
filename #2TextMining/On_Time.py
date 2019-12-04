from datetime import datetime
import pymysql
import time
import numpy as np
import pandas as pd

#Declare Connection
conn = pymysql.connect(host='localhost', port='', user='root', passwd='', db='tes_coba', use_unicode=True, charset="utf8mb4")
cur = conn.cursor()

EW = "Tepat Waktu"
LW = "Tidak Tepat Waktu"

#get data from database
cur.execute("SELECT * FROM `tweet2`")
row1 = cur.fetchall()

n  = 1

for record in row1:
    if record[2] > record[5]: # I'm assuming the column index 2 and 5 have the relevant table column values
        Result = EW
    elif record[2] < record[5]:
        Result = LW
    
    print(Result)
    cur.execute("UPDATE tweet2 SET on_time=%s WHERE no=%s",(str(Result), str(n)))
    n = n + 1

    
conn.commit()
cur.close()
conn.close()
