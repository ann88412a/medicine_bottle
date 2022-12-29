from flask import Flask, render_template, request, url_for, redirect, Response, session, make_response
from datetime import timedelta
import time
import numpy as np









app = Flask(__name__)

medicine_list = []
medicine_dict = {}

@app.route('/syringe/<username>')
def init(username):
    print("welcome", username)
    print("="*20 + "init" + "="*20)
    global medicine_dict
    medicine_dict[username] = []
    # medicine_dict["kigison"] = [['a', 'b', 'c', 'd', 'e']]  # use for test
    resp = make_response(redirect(url_for(r'syringe_index')))
    resp.set_cookie('username', username)  # save username in cookies
    return resp

@app.route('/syringe/syringe_index/')
def syringe_index():
    global medicine_dict
    # print(medicine_dict)
    # print(request.cookies.get('username'))
    return render_template(r"syringe/syringe_index.html", medicine_list=medicine_dict[request.cookies.get('username')])

@app.route('/syringe/barcode/', methods=['POST','GET'])
def barcode():
    if request.method == 'POST':
        global medicine_list
        # if request.values['send'] == 'next':
        barcode_id = request.values['barcode']
        print("barcode_id:", barcode_id)
        # medicine_arr.append([barcode_id])
        medicine_list.append([barcode_id, barcode_id, barcode_id])
        return render_template(r'syringe/barcode.html', barcode_id=barcode_id)
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port="8787", debug=True)