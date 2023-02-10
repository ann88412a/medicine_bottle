import pymysql

print('hi')

db = pymysql.connect(host='localhost', port=3306, user='root', passwd='pcs54784', db='yangming', charset='utf8')
#建立操作游標
cursor = db.cursor()
#SQL語法（查詢資料庫版本）
sql = 'SELECT VERSION()'
#執行語法
cursor.execute(sql)
#選取第一筆結果
data = cursor.fetchone()

print ("Database version : %s " % data)

#SQL語法（查詢資料庫版本）
sql = 'select * from test;'
#執行語法
cursor.execute(sql)
#選取第一筆結果
data = cursor.fetchone()

print (data[0])
#關閉連線
db.close()
