import time, random, requests
import DAN , os
import threading

#================iottalk===============
ServerURL = 'https://1.iottalk.tw'      #with non-secure connection
#ServerURL = 'https://DomainName' #with SSL connection
Reg_addr = 'MedicationTalk_Device0' #if None, Reg_addr = MAC address
DAN.profile['d_name'] = 'MedicationTalk_Device0'


DAN.device_registration_with_retry(ServerURL, Reg_addr)

while True:
    try:
        #IDF_data = random.uniform(1, 10)
        #DAN.push ('Dummy_Sensor', IDF_data) #Push data to an input device feature "Dummy_Sensor"

        #==================================
        
        print(DAN.pull('Barcode-O'))
        
        

    except Exception as e:
        print(e)
        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr is not found. Try to re-register...')
            DAN.device_registration_with_retry(ServerURL, Reg_addr)
        else:
            print('Connection failed due to unknow reasons.')
            time.sleep(1)    

    time.sleep(0.2)