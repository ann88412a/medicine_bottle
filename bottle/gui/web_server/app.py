from flask import Flask, render_template, request, url_for, redirect, make_response
from threading import Thread
from iottalk_lib import DAN
import time, json, random, string, sys
import numpy as np

hist_dict = {}  # {userID:[[Barcode, Medicine name, Dosage, Diluted doses, Injection site], ...], ...}
pull_data = {"barcode": {}, "syringe": {}}
medicine_dict = {"4710031116149": "AMIKACIN INJECTION 250MG/ML 'TAI YU'",  # Group 1
                 "4710031297121": "Heparin Sodium Injection 5000 IU/ml 'Tai Yu'",
                 "4710596700920": "CEFAZOLIN INJECTION 1GM 'C.C.P.'",
                 "3582910008934": "CORDARONE INJECTION",
                 "4719858031321": "SODIUM BICARBONATE INJECTION 'CHI SHENG'",
                 "4711916010354": "ROLIKAN INJECTION (SODIUM BICARBONATE)",
                 # "4710031116149": "AMIKACIN INJECTION 250MG/ML 'TAI YU'",  # Group 2
                 "4711457371105": "Sirolac IV Injection 30 mg/ml 'ASTAR'",
                 "4710596702344": "Oxacillin Powder for Injection 'CYH'",  # Group 3
                 "4719858033455": "Progesterone Injection 'Chi Sheng'",
                 "108806520004816": "CLEXANE INJECTION",
                 "4715550032017": "AMPOLIN INJECTION 500MG",  # Group 4
                 "4987170870854": "MILLISROL INJECTION"}


app = Flask(__name__)

@app.route('/syringe/', defaults={'machine_id': 'bottle_01', 'username': 'undefine'})
@app.route('/syringe/<machine_id>/<username>')
def init(machine_id, username):
    global hist_dict
    resp = make_response(redirect(url_for(r'syringe_index')))
    # print(request.cookies.get('userID'))
    if(request.cookies.get('userID') != "None"):
        try:
            if hist_dict[request.cookies.get('userID')] != []:
                return resp
        except:
            pass

    N = 12  ## len(userID)
    userID = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))
    hist_dict[userID] = []
    resp.set_cookie('userID', userID, samesite='None', secure=True)  # save userID in cookies
    resp.set_cookie('machine_id', machine_id, samesite='None', secure=True)
    resp.set_cookie('username', username, samesite='None', secure=True)
    print("welcome", userID)
    return resp

@app.route('/syringe/syringe_index/')
def syringe_index():
    global hist_dict
    # print(request.cookies)
    show_log = r"\n"*10+r"(#`Д´)ﾉ  跨殺洨  (#`Д´)ﾉ\n\n是想作弊膩  ಠ_ಠ\n\n再不離開我叫老師來了喔!\n     .......(￣０￣)ノ舉手"+r"\n"*10
    resp = make_response(render_template(r"syringe/syringe_index.html", medicine_list=hist_dict[request.cookies.get('userID')], show_log=show_log))
    resp.set_cookie('random_id', str(time.time()), samesite='None', secure=True)  # save random_id in cookies. use for unit.
    resp.set_cookie('barcode_id', "None", samesite='None', secure=True)  # save random_id in cookies. use for unit.
    resp.set_cookie('syringe_diluent_value', "None", samesite='None', secure=True)
    resp.set_cookie('syringe_type', "None", samesite='None', secure=True)
    resp.set_cookie('syringe_scale_value', "None", samesite='None', secure=True)
    resp.set_cookie('injection_info', "None", samesite='None', secure=True)
    # print(hist_dict)
    return resp

@app.route('/syringe/add_new/', methods=['POST','GET'])
def add_new():
    global hist_dict
    if request.method == 'POST':
        if request.values['barcode_scan_state'] == '1':
            DAN.push('barcode_control_server', request.cookies.get('machine_id'),
                     request.cookies.get('random_id'), True)
            return redirect(url_for(r'wait_data'))
        elif request.values['syringe_diluent_state'] == '1':
            resp = make_response(redirect(url_for(r'add_new')))
            resp.set_cookie('syringe_diluent_value', request.values['syringe_diluent_value'], samesite='None', secure=True)
            return resp
        elif request.values['syringe_scan_state'] == '1':
            DAN.push('syringe_scale_control_server', request.cookies.get('machine_id'), request.cookies.get('random_id'), request.values['syringe_type'], True)
            return redirect(url_for(r'wait_data'))
        elif request.values['injection_info_state'] == '1':
            resp = make_response(redirect(url_for(r'add_new')))

            if request.values['injection_info_site'] != "-":
                __injection_info = "{}({})".format(request.values['injection_info'], request.values['injection_info_site'])
            else:
                __injection_info = request.values['injection_info']
            resp.set_cookie('injection_info', __injection_info, samesite='None', secure=True)  # save random_id in cookies. use for unit.
            return resp
        elif request.values['add_new_state'] == '1':
            usr = request.cookies.get('userID')
            Barcode = request.cookies.get('barcode_id')
            try:
                Medicine_name = medicine_dict[Barcode]
            except:
                Medicine_name = "查無此藥品"
            Diluted_doses = request.cookies.get('syringe_diluent_value')
            Dosage = request.cookies.get('syringe_scale_value')
            injection_info = request.cookies.get('injection_info')
            # print([Barcode, Medicine_name, Diluted_doses, Dosage, injection_info])
            if len(hist_dict[usr]) > 0:
                same_barcode_index_arr = np.where(np.array(hist_dict[usr].copy())[:, 0] == Barcode)[0]
                if(same_barcode_index_arr.size != 0):
                    __idx = same_barcode_index_arr[0]
                    hist_dict[usr][__idx][2] = str(float(hist_dict[usr][__idx][2]) + float(Diluted_doses))  # Diluted_doses
                    hist_dict[usr][__idx][3] = str(float(hist_dict[usr][__idx][3]) + float(Dosage))  # Dosage
                    if hist_dict[usr][__idx][4] != injection_info:
                        hist_dict[usr][__idx][4] = "{} / {}".format(hist_dict[usr][__idx][4], injection_info)
                else:
                    hist_dict[usr].append([Barcode, Medicine_name, Diluted_doses, Dosage, injection_info])
            else:
                hist_dict[usr].append([Barcode, Medicine_name, Diluted_doses, Dosage, injection_info])
            return redirect(url_for(r'syringe_index'))

    return render_template(r'syringe/add_new_medicine.html', medicine_dict=medicine_dict)

@app.route('/syringe/wait_data/', methods=['POST', 'GET'])
def wait_data():
    global pull_data
    if request.cookies.get('random_id') in pull_data["barcode"].keys():
        resp = make_response(redirect(url_for(r'add_new')))
        resp.set_cookie('barcode_id', str(pull_data["barcode"][request.cookies.get('random_id')]), samesite='None', secure=True)
        del pull_data["barcode"][request.cookies.get('random_id')]
        return resp
    if request.cookies.get('random_id') in pull_data["syringe"].keys():
        resp = make_response(redirect(url_for(r'add_new')))
        resp.set_cookie('syringe_type', pull_data["syringe"][request.cookies.get('random_id')][-2], samesite='None', secure=True)
        resp.set_cookie('syringe_scale_value', str(pull_data["syringe"][request.cookies.get('random_id')][-1]), samesite='None', secure=True)
        del pull_data["syringe"][request.cookies.get('random_id')]
        return resp

    if request.method == 'POST':
        if request.values['cancel_scale'] == '1':
            DAN.push('barcode_control_server', request.cookies.get('machine_id'),
                     request.cookies.get('random_id'), False)
            DAN.push('syringe_scale_control_server', request.cookies.get('machine_id'),
                     request.cookies.get('random_id'), request.cookies.get('syringe_type'), False)
            return redirect(url_for(r'add_new'))
        if request.values['refresh'] == '1':
            return ("", 204)
    return render_template(r'syringe/wait_data.html', barcode_id=None, medicine_name=None)

@app.route('/syringe/submit_result/')
def submit_result():
    global hist_dict, pull_data
    try:
        push_data = json.dumps({"bottle": hist_dict[request.cookies.get('userID')]})
        DAN.push('syringe_submit_result_server', push_data)
        # print("DAN.push('syringe_submit_result_server')", push_data)
        del hist_dict[request.cookies.get('userID')]

    except KeyError:
        pass
    # return redirect("http://140.113.110.21:1526/show/index.html", code=302)  # Enter the URL you wish to use after push data.
    # print(hist_dict, pull_data)
    # return redirect(url_for(r'init'))
    return render_template(r"syringe/finished.html")

@app.route('/syringe/RESET')
def RESET():
    global hist_dict, pull_data
    hist_dict = {}
    pull_data = {"barcode": {}, "syringe": {}}
    print("Reset Successfully!")
    return "Reset Successfully!"

## =============================================================
def dummy_device_loop():
    global pull_data
    ServerURL = __cfg["ServerURL"]  # with non-secure connection
    # ServerURL = 'https://DomainName' #with SSL connection
    Reg_addr = __cfg["Reg_addr"]  # if None, Reg_addr = MAC address
    DAN.profile['dm_name'] = 'medical_bottle_server_V2'
    DAN.profile['df_list'] = ['barcode_control_server', 'syringe_scale_control_server', 'syringe_submit_result_server', 'barcode_result_server',
                              'syringe_scale_result_server', ]
    DAN.profile['d_name'] = __cfg["d_name"]
    DAN.device_registration_with_retry(ServerURL, Reg_addr)
    # DAN.deregister()  #if you want to deregister this device, uncomment this line
    # exit()            #if you want to deregister this device, uncomment this line
    while True:
        try:
            barcode_result = DAN.pull('barcode_result_server')  # Pull data from an output device feature "Dummy_Control"
            if barcode_result != None:  ## barcode_result -> [UserName, RandId, BarcodeResult]
                # if barcode_result[-1] == True:
                #     DAN.push('barcode_control_server', request.cookies.get('userID'),
                #              request.cookies.get('random_id'), False)
                # print('barcode_result', barcode_result)
                pull_data["barcode"][barcode_result[1]] = barcode_result[-1]
            syringe_scale_result = DAN.pull('syringe_scale_result_server')  # Pull data from an output device feature "Dummy_Control"
            if syringe_scale_result != None:  ## syringe_scale_result -> [UserName, RandId, SyringeType, Dosage]
                # print('syringe_scale_result', syringe_scale_result)
                pull_data["syringe"][syringe_scale_result[1]] = syringe_scale_result[2:]

        except Exception as e:
            print(e)
            if str(e).find('mac_addr not found:') != -1:
                print('Reg_addr is not found. Try to re-register...')
                DAN.device_registration_with_retry(ServerURL, Reg_addr)
            else:
                print('Connection failed due to unknow reasons.')
                time.sleep(1)
        time.sleep(0.2)




if __name__ == '__main__':
    cfg_file_path = "/home/pcs-file-server/Documents/cfg_files/web_server.cfg"
    with open(cfg_file_path, 'r') as __f:
        __cfg = json.load(__f)
        __f.close()
    dm_loop = Thread(target=dummy_device_loop, name="medical_iottalk")
    dm_loop.setDaemon(True)
    dm_loop.start()
    # font - family: verdana;
    app.run(host='0.0.0.0', port=__cfg["flask_port"], debug=__cfg["flask_debug"])
    # app.run(host='0.0.0.0', port="8100", ssl_context=('D:/medical_ssl/server.crt', 'D:/medical_ssl/server.key'), debug=False)



    # https://freemyip.com/update?token=6c45fd4a1593f4a16b1f9803&domain=medical.freemyip.com&verbose=yes
