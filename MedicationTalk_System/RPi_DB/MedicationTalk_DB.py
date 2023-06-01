'''
MedicationTalk Raspberry Pi DataBase
Deployment: Raspberry Pi
說明：提供資料庫查詢分析功能與 IoTtalk 交互
Features：
1. Barcode 資訊： 查詢 Barcode 資訊
2. 紀錄檢定成績： 儲存檢定的學生及檢定資訊
3. 查詢分析歷史成績： 查詢特定情境的資訊回傳至 Platform 圖表
'''

import time, random, requests
import DB_DAN, Platform_DAN, csmapi, os
import threading
import pymysql
import datetime
import json

#================iottalk===============
ServerURL = 'https://1.iottalk.tw'     
csmapi.ENDPOINT = ServerURL

# set DB dummy device
DB_Reg_addr = 'DataBase_0' #if None, Reg_addr = MAC address
DB_DAN.profile['d_name'] = 'DataBase_0'
DB_DAN.device_registration_with_retry(ServerURL, DB_Reg_addr)

# set Platform dummy device
# Platform_Reg_addr = 'Medication_Platform_0' #if None, Reg_addr = MAC address
# Platform_DAN.profile['d_name'] = 'Medication_Platform_0'
# Platform_DAN.device_registration_with_retry(ServerURL, Platform_Reg_addr)

# connect DB
db = pymysql.connect(host='localhost', port=3306, user='root', passwd='pcs54784', db='yangming', charset='utf8')
cursor = db.cursor()

# init
user_id = 'user'
watchdog = 0

# loop communicate with IoTtalk
while True:
    try:
        # watchdog make sure device register
        watchdog = watchdog + 1
        
        if (watchdog > 1000):
            db.close()
            db = pymysql.connect(host='localhost', port=3306, user='root', passwd='pcs54784', db='yangming', charset='utf8')
            cursor = db.cursor()
            DB_DAN.device_registration_with_retry(ServerURL, DB_Reg_addr)
            # Platform_DAN.device_registration_with_retry(ServerURL, Platform_Reg_addr)
            watchdog = 0

        # pull IoTtalk info

        # barcode
        barcode = DB_DAN.pull('Retrieve-O')
        
        if barcode != None:
            # user identify
            user_uid = barcode[0]
            if barcode[1] == 'patient':
                # sql cmd
                sql = "select info from patient_info where barcode='" + barcode[2] + "';"
                cursor.execute(sql)
                data = cursor.fetchall()

                if (len(data) > 0):
                    barcode_dict = {'patient_info':  data[0][0], 'barcode_value': barcode[2]}
                    barcode_json = json.dumps(barcode_dict)
                    DB_DAN.push ('Barcode_Result-I', user_uid, barcode_json)
                else:
                    barcode_dict = {'patient_info': '查無此病人資訊', 'barcode_value': barcode[2]}
                    barcode_json = json.dumps(barcode_dict)
                    DB_DAN.push ('Barcode_Result-I', user_uid, barcode_json)

            elif barcode[1] == 'syringe':
                sql = "select * from syringe_barcode where barcode='" + barcode[2] + "';"
                cursor.execute(sql)
                data = cursor.fetchall()

                if (len(data) > 0):
                    medicine_dict = {
                        'medicine_info' : data[0][0]
                    }
                    barcode_json = json.dumps(medicine_dict)

                    DB_DAN.push ('Barcode_Result-I', user_uid, barcode_json)
                else:
                    medicine_dict = {
                        'medicine_info' : '查無此藥品資訊'
                    }
                    barcode_json = json.dumps(medicine_dict)

                    DB_DAN.push ('Barcode_Result-I', user_uid, barcode_json)
        # sheet 
        # record exam info to SQL
        sheet = DB_DAN.pull('Sheet-O')

        if sheet != None:
            # time
            now = datetime.datetime.now()
            now = now.strftime('%Y-%m-%d-%H-%M-%S')

            # info
            data = json.loads(sheet[0])

            # sql cmd
            sql = "insert into record value(" + str(data['class']) + ", '" + str(data['id']) + "', '" + str(data['name']) + "', '" + str(data['barcode1']) + "', '" + str(data['select1']) + "', "  + str(data['correctness1']) + ", '"
            sql = sql + str(data['check2']) + "', " + str(data['Dilatrend']) + ", " + str(data['Dilantin']) + ", " + str(data['correctness2']) + ", '" + str(data['reason2']) + "', '"
            sql = sql + str(data['check3']) + "', " + str(data['Requip']) + ", " + str(data['Requip1']) + ", " + str(data['correctness3']) + ", '" + str(data['reason3']) + "', '"
            sql = sql + str(data['check4']) + "', " + str(data['correctness4']) + ", '" + str(data['reason4']) + "', '"
            sql = sql + str(data['check5']) + "', " + str(data['Repaglinide']) + ", " + str(data['correctness5']) + ", '" + str(data['reason5']) + "', '"
            sql = sql + str(data['check6']) + "', " + str(data['Transamin']) + ", " + str(data['correctness6']) + ", '" + str(data['reason6']) + "', '"
            sql = sql + str(data['check7']) + "', " + str(data['correctness7']) + ", '" + str(data['reason7']) + "', '"
            sql = sql + str(data['check8']) + "', " + str(data['Bokey']) + ", " + str(data['correctness8']) + ", '" + str(data['reason8']) + "', '"
            sql = sql + str(data['check9']) + "', " + str(data['Simvahexal']) + ", " + str(data['correctness9']) + ", '" + str(data['reason9']) + "', '"
            sql = sql + str(data['check10']) + "', " + str(data['FLU']) + ", " + str(data['correctness10']) + ", '" + str(data['reason10']) + "', '"    
            
            sql = sql + now + "', '" + str(data['uid']) + "');"
            
            cursor.execute("use yangming;")
            cursor.execute(sql)
            # same db
            db.commit()


        # analysis page search
        search = DB_DAN.pull('Search-O')

        if search != None:
            user_uid = search[0]
            data = json.loads(search[1])

            # pie chart
            if data['operation'] == 'level':
                level_num = [0, 0, 0] # low, mid, high
                sql = "select 1_correctness, 2_correctness, 3_correctness, 4_correctness, 5_correctness, 6_correctness, 7_correctness, 8_correctness, 9_correctness, 10_correctness from record ;"
                cursor.execute(sql)
                result = cursor.fetchall()

                for each_record in result:
                    total_score = sum(list(filter(lambda x: x < 2, each_record)))

                    if total_score >= 7:
                        level_num[2] = level_num[2] + 1
                    elif total_score >= 4:
                        level_num[1] = level_num[1] + 1
                    else: 
                        level_num[0] = level_num[0] + 1

                push_item = {"operation": 'level', "level": level_num,}
                
                #轉成 json 字串
                push_item = json.dumps(push_item)

                DB_DAN.push ('Search_Result-I', user_uid, push_item)

            # line chart
            if data['operation'] == 'history':
                history_data = []
                history_data.clear()
                history_label = []
                history_label.clear()

                # sql cmd
                sql = "select 1_correctness, 2_correctness, 3_correctness, 4_correctness, 5_correctness, 6_correctness, 7_correctness, 8_correctness, 9_correctness, 10_correctness from record where id='" + data['id'] + "';"
                cursor.execute(sql)
                
                result = cursor.fetchall()

                for each_record in result:
                    total_score = sum(list(filter(lambda x: x < 2, each_record)))
                    history_data.append(total_score)

                # sql cmd
                sql = "SELECT time FROM record where id='" + data['id'] + "';"
                cursor.execute(sql)
                result = cursor.fetchall()
                
                for each_record in result:
                    history_label.append(each_record[0])
                
                push_item = {"operation": 'history', "history_data": history_data, "history_label": history_label,}
                
                #轉成 json 字串
                push_item = json.dumps(push_item)
                
                DB_DAN.push ('Search_Result-I', user_uid, push_item)
                
            # bar chart
            if data['operation'] == 'time_total':
                each_q_score = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            
                # sql cmd
                sql = "SELECT 1_correctness, 2_correctness, 3_correctness, 4_correctness, 5_correctness, 6_correctness, 7_correctness, 8_correctness, 9_correctness, 10_correctness FROM record where "
                sql = sql + "(cast(substring(time, 6, 2) as unsigned) = " + str(int(data["start_date"][5:7])) + " and cast(substring(time, 9, 2) as unsigned) >= " + str(int(data["start_date"][8:10])) + ")"
                sql = sql + "or (cast(substring(time, 6, 2) as unsigned) > " + str(int(data["start_date"][5:7])) + " and cast(substring(time, 6, 2) as unsigned) < " + str(int(data["start_date"][5:7])) + ")"
                sql = sql + " or (cast(substring(time, 6, 2) as unsigned) = " + str(int(data["end_date"][5:7])) + " and cast(substring(time, 9, 2) as unsigned) <= " + str(int(data["end_date"][8:10])) + ");"
                
                cursor.execute(sql)
                result = cursor.fetchall()

                for each_record in result:
                    for i in range(len(each_record)):
                        if (each_record[i] == 1):
                            each_q_score[i] = each_q_score[i] + 1

                push_item = {"operation": 'time_total', "each_q_score": each_q_score,}
                
                #轉成 json 字串
                push_item = json.dumps(push_item)
 
                DB_DAN.push ('Search_Result-I', user_uid, push_item)

    except Exception as e:
        print(e)
        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr is not found. Try to re-register...')
            DB_DAN.device_registration_with_retry(ServerURL, DB_Reg_addr)
            # Platform_DAN.device_registration_with_retry(ServerURL, Platform_Reg_addr)
        else:
            print('Connection failed due to unknow reasons.')
            time.sleep(1)    

    time.sleep(0.5)