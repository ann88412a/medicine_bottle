from flask import Flask, render_template, request, url_for, redirect, Response, make_response
from datetime import timedelta
import time
import numpy as np


# medicine_list = []
hist_dict = {}  # {username:[[Barcode, Medicine name, Dosage, Diluted doses, Injection site], ...], ...}
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



@app.route('/syringe/<username>')
def init(username):
    print("welcome", username)
    print("="*20 + "init" + "="*20)
    global hist_dict
    hist_dict[username] = []
    # hist_dict["kigison"] = [[1,2,3,4,5]]  # use for test
    resp = make_response(redirect(url_for(r'syringe_index')))
    resp.set_cookie('username', username)  # save username in cookies
    return resp

@app.route('/syringe/syringe_index/')
def syringe_index():
    global hist_dict
    # print(hist_dict)
    # print(request.cookies.get('username'))
    return render_template(r"syringe/syringe_index.html", medicine_list=hist_dict[request.cookies.get('username')])

@app.route('/syringe/add_new/')
def add_new():
    return render_template(r'syringe/add_new_medicine.html', barcode_id=None, medicine_name=None)


@app.route('/syringe/barcode/')
def barcode():
    # dai.push('df_name_barcode_sw', [request.cookies.get('username'), True])
    # barcode_id = dai.pull()
    # t = time.time()
    # while(True):
    #     if (time.time()-t) > 5:
    #         break
    barcode_id = "4715550032017"
    global hist_dict
    usr = request.cookies.get('username')
    ## hist_dict[usr][len(hist_dict[usr])-1]  # 最後一筆
    hist_dict[usr].append([barcode_id])
    hist_dict[usr][len(hist_dict[usr])-1].append(medicine_dict[barcode_id])
    # print("barcode_id:", barcode_id)
    return render_template(r'syringe/barcode.html', barcode_id="")

@app.route('/syringe/diluent/')
def diluent():
    return render_template(r'syringe/diluent.html')

@app.route('/syringe/scale/', methods=['POST','GET'])
def scale():
    if request.method == 'POST':
        # if request.values['send'] == 'next':
        syringe_type = request.values['syringe_type']
        print("syringe_type:", syringe_type)
        return render_template(r'syringe/scale.html', syringe_type=syringe_type)
    return render_template(r'syringe/scale.html', syringe_type="")


@app.route('/syringe/submit_result/')
def submit_result():
    try:
        # del hist_dict[request.cookies.get('username')]
        print("del hist_dict[request.cookies.get('username')]")
    except KeyError:
        pass
    return redirect("https://www.google.com", code=302)  # Enter the URL you wish to use after push data.






if __name__ == '__main__':
    app.run(host='0.0.0.0', port="8787", debug=True)