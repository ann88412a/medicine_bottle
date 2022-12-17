import time, random, requests
import DAN , csmapi, os
import threading

#================iottalk===============
ServerURL = 'https://6.iottalk.tw'      #with non-secure connection
#ServerURL = 'https://DomainName' #with SSL connection
Reg_addr = 'BAC0B21FDC33' #if None, Reg_addr = MAC address

csmapi.ENDPOINT = ServerURL
# DAN.device_registration_with_retry(ServerURL, Reg_addr)

while True:
    try:
        #IDF_data = random.uniform(1, 10)
        barcode_ans = '310832007'
        DAN.push ('barcode_ans', barcode_ans) #Push data to an input device feature "Dummy_Sensor"

        #==================================
        pill_detect_check = DAN.pull('pill_detect_check')#Pull data from an output device feature "Dummy_Control"
        print(pill_detect_check)
        
        

    except Exception as e:
        print(e)
        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr is not found. Try to re-register...')
            DAN.device_registration_with_retry(ServerURL, Reg_addr)
        else:
            print('Connection failed due to unknow reasons.')
            time.sleep(1)    

    time.sleep(0.5)