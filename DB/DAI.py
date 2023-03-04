import time, random, requests
import DAN , csmapi, os
import threading
import pymysql
import datetime
import json

#================iottalk===============
ServerURL = 'https://1.iottalk.tw'      #with non-secure connection
#ServerURL = 'https://DomainName' #with SSL connection
Reg_addr = 'FF2C3883758D' #if None, Reg_addr = MAC address

csmapi.ENDPOINT = ServerURL
# DAN.device_registration_with_retry(ServerURL, Reg_addr)
user_id = 'user'
# DB
db = pymysql.connect(host='localhost', port=3306, user='root', passwd='pcs54784', db='yangming', charset='utf8')
cursor = db.cursor()


while True:
    try:
        barcode = DAN.pull('Barcode-O')
        
        if barcode != None:
            print(barcode)
            user_uid = barcode[0]
            sql = "select info from patient_info where barcode='" + barcode[1] + "';"
            cursor.execute(sql)
            data = cursor.fetchall()
            if (len(data) > 0):
                DAN.push ('Patient-I', user_uid, data[0][0])
            else:
                DAN.push ('Patient-I', user_uid, '查無此病人資訊')
        

        sheet = DAN.pull('Sheet-O')

        if sheet != None:
            now = datetime.datetime.now()
            now = now.strftime('%Y_%m_%d_%H_%M_%S')

            # print(sheet[0])
            data = json.loads(sheet[0])

            # sql = "insert into record(class, id, name, 1_barcode, 1_select, 1_correctness, "
            # sql = sql + "2_check, 2_Dilatrend, 2_Dilantin, 2_correctness, 2_reason, "
            # sql = sql + "3_check, 3_Requip, 3_Requip1, 3_correctness, 3_reason, "
            # sql = sql + "4_check, 4_correctness, "
            # sql = sql + "5_check, 5_Repaglinide, 5_correctness, 5_reason, "
            # sql = sql + "6_check, 6_Transamin, 6_correctness, 6_reason, "
            # sql = sql + "7_check, 7_correctness, "
            # sql = sql + "8_check, 8_Bokey, 8_correctness, 8_reason, "
            # sql = sql + "9_check, 9_Zocor, 9_correctness, 9_reason, "
            # sql = sql + "10_check, 10_FLU, 10_correctness, 10_reason, time) value("

            sql = "insert into record value(" + str(data['class']) + ", '" + str(data['id']) + "', '" + str(data['name']) + "', '" + str(data['barcode1']) + "', '" + str(data['select1']) + "', "  + str(data['correctness1']) + ", '"
            sql = sql + str(data['check2']) + "', " + str(data['Dilatrend']) + ", " + str(data['Dilantin']) + ", " + str(data['correctness2']) + ", '" + str(data['reason2']) + "', '"
            sql = sql + str(data['check3']) + "', " + str(data['Requip']) + ", " + str(data['Requip1']) + ", " + str(data['correctness3']) + ", '" + str(data['reason3']) + "', '"
            sql = sql + str(data['check4']) + "', " + str(data['correctness4']) + ", '"
            sql = sql + str(data['check5']) + "', " + str(data['Repaglinide']) + ", " + str(data['correctness5']) + ", '" + str(data['reason5']) + "', '"
            sql = sql + str(data['check6']) + "', " + str(data['Transamin']) + ", " + str(data['correctness6']) + ", '" + str(data['reason6']) + "', '"
            sql = sql + str(data['check7']) + "', " + str(data['correctness7']) + ", '"
            sql = sql + str(data['check8']) + "', " + str(data['Bokey']) + ", " + str(data['correctness8']) + ", '" + str(data['reason8']) + "', '"
            sql = sql + str(data['check9']) + "', " + str(data['Simvahexal']) + ", " + str(data['correctness9']) + ", '" + str(data['reason9']) + "', '"
            sql = sql + str(data['check10']) + "', " + str(data['FLU']) + ", " + str(data['correctness10']) + ", '" + str(data['reason10']) + "', '"    
            

            sql = sql + now + "', '" + str(data['uid']) + "');"
            print(sql)
            
            # sql = "INSERT INTO record (class, id, name, 1_barcode, 1_select, 1_correctness, 2_check, 2_Dilatrend, 2_Dilantin, 2_correctness, 2_reason, 3_check, 3_Requip, 3_Requip1, 3_correctness, 3_reason, 4_check, 4_correctness, 5_check, 5_Repaglinide, 5_correctness, 5_reason, 6_check, 6_Transamin, 6_correctness, 6_reason, 7_check, 7_correctness, ) VALUES (%s, %s)"
            
            cursor.execute("use yangming;")
            print(cursor.fetchall())
            cursor.execute(sql)
            print(cursor.fetchall())
            cursor.execute("select * from record;")
            print(cursor.fetchall())





        
        

    except Exception as e:
        print(e)
        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr is not found. Try to re-register...')
            DAN.device_registration_with_retry(ServerURL, Reg_addr)
        else:
            print('Connection failed due to unknow reasons.')
            time.sleep(1)    

    time.sleep(0.5)