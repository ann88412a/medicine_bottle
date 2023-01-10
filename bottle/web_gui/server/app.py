from flask import Flask, render_template, request, url_for, redirect, make_response
from threading import Thread
from iottalk_lib import DAN
import time, json, random, string

hist_dict = {}  # {username:[[Barcode, Medicine name, Dosage, Diluted doses, Injection site], ...], ...}
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



@app.route('/syringe/')
def init():
    N = 16  ## len(username)
    username = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))
    print("welcome", username)
    global hist_dict
    hist_dict[username] = []
    # hist_dict["kigison"] = [[1,2,3,4,5]]  # use for test
    resp = make_response(redirect(url_for(r'syringe_index')))
    resp.set_cookie('username', username)  # save username in cookies
    return resp

@app.route('/syringe/syringe_index/')
def syringe_index():
    global hist_dict
    resp = make_response(render_template(r"syringe/syringe_index.html", medicine_list=hist_dict[request.cookies.get('username')]))
    resp.set_cookie('random_id', str(time.time()))  # save random_id in cookies. use for unit.
    resp.set_cookie('barcode_id', "None")  # save random_id in cookies. use for unit.
    resp.set_cookie('syringe_diluent_value', "None")
    resp.set_cookie('syringe_type', "None")
    resp.set_cookie('syringe_scale_value', "None")
    resp.set_cookie('injection_site', "None")
    return resp

@app.route('/syringe/add_new/', methods=['POST','GET'])
def add_new():
    global hist_dict
    if request.method == 'POST':
        if request.values['barcode_scan_state'] == '1':
            DAN.push('barcode_control_server', request.cookies.get('username'),
                     request.cookies.get('random_id'), True)
            return redirect(url_for(r'wait_data'))
        elif request.values['syringe_scan_state'] == '1':
            DAN.push('syringe_scale_control_server', request.cookies.get('username'),
                     request.cookies.get('random_id'), request.values['syringe_diluent_value'],
                     request.values['syringe_type'], True)
            return redirect(url_for(r'wait_data'))
        elif request.values['injection_site_state'] == '1':
            resp = make_response(redirect(url_for(r'add_new')))
            resp.set_cookie('injection_site', request.values['injection_site'])  # save random_id in cookies. use for unit.
            return resp
        elif request.values['add_new_state'] == '1':
            usr = request.cookies.get('username')
            Barcode = request.cookies.get('barcode_id')
            Medicine_name = medicine_dict[Barcode]
            Dosage = request.cookies.get('syringe_scale_value')
            Diluted_doses = request.cookies.get('syringe_diluent_value')
            Injection_site = request.cookies.get('injection_site')
            print([Barcode, Medicine_name, Dosage, Diluted_doses, Injection_site])
            hist_dict[usr].append([Barcode, Medicine_name, Dosage, Diluted_doses, Injection_site])
            return redirect(url_for(r'syringe_index'))

    return render_template(r'syringe/add_new_medicine.html', medicine_dict=medicine_dict)


@app.route('/syringe/wait_data/')
def wait_data():
    global pull_data
    if request.cookies.get('random_id') in pull_data["barcode"].keys():
        resp = make_response(redirect(url_for(r'add_new')))
        resp.set_cookie('barcode_id', str(pull_data["barcode"][request.cookies.get('random_id')]))
        del pull_data["barcode"][request.cookies.get('random_id')]
        return resp
    if request.cookies.get('random_id') in pull_data["syringe"].keys():
        resp = make_response(redirect(url_for(r'add_new')))
        resp.set_cookie('syringe_diluent_value', str(pull_data["syringe"][request.cookies.get('random_id')][-3]))
        resp.set_cookie('syringe_type', pull_data["syringe"][request.cookies.get('random_id')][-2])
        resp.set_cookie('syringe_scale_value', str(pull_data["syringe"][request.cookies.get('random_id')][-1]))
        del pull_data["syringe"][request.cookies.get('random_id')]
        return resp
    if request.cookies.get('injection_site') != "None":
        return render_template(r'syringe/add_new_medicine.html', medicine_dict=medicine_dict)
    return render_template(r'syringe/wait_data.html', barcode_id=None, medicine_name=None)

@app.route('/syringe/submit_result/')
def submit_result():
    global hist_dict
    try:
        push_data = json.dumps({"bottle": hist_dict[request.cookies.get('username')]})
        DAN.push('syringe_submit_result_server', push_data)
        print("DAN.push('syringe_submit_result_server')", push_data)
        del hist_dict[request.cookies.get('username')]

    except KeyError:
        pass
    return redirect("http://140.113.110.21:1526/show/index.html", code=302)  # Enter the URL you wish to use after push data.


## =============================================================
def dummy_device_loop():
    global pull_data
    ServerURL = 'http://1.iottalk.tw:9999'  # with non-secure connection
    # ServerURL = 'https://DomainName' #with SSL connection
    Reg_addr = None  # if None, Reg_addr = MAC address
    DAN.profile['dm_name'] = 'medical_bottle_server'
    DAN.profile['df_list'] = ['barcode_control_server', 'syringe_scale_control_server', 'syringe_submit_result_server', 'barcode_result_server',
                              'syringe_scale_result_server', ]
    DAN.profile['d_name'] = 'medical_bottle_server'
    DAN.device_registration_with_retry(ServerURL, Reg_addr)
    # DAN.deregister()  #if you want to deregister this device, uncomment this line
    # exit()            #if you want to deregister this device, uncomment this line
    while True:
        try:
            barcode_result = DAN.pull('barcode_result_server')  # Pull data from an output device feature "Dummy_Control"
            if barcode_result != None:  ## barcode_result -> [UserName, RandId, BarcodeResult]
                # if barcode_result[-1] == True:
                #     DAN.push('barcode_control_server', request.cookies.get('username'),
                #              request.cookies.get('random_id'), False)
                print('barcode_result', barcode_result)
                pull_data["barcode"][barcode_result[1]] = barcode_result[-1]
            syringe_scale_result = DAN.pull('syringe_scale_result_server')  # Pull data from an output device feature "Dummy_Control"
            if syringe_scale_result != None:  ## syringe_scale_result -> [UserName, RandId, DilutedDoses, SyringeType, Dosage]
                print('syringe_scale_result', syringe_scale_result)
                pull_data["syringe"][syringe_scale_result[1]] = syringe_scale_result[-3:]

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
    Thread(target=dummy_device_loop).start()


    # app.run(host='0.0.0.0', port="54784", debug=True)
    app.run(host='0.0.0.0', port="54784", debug=False)