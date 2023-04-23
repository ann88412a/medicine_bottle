from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_cors import CORS
import time

 
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ["https://fritingo.github.io"]}}) 

from sqlalchemy import create_engine, text, or_
from sqlalchemy.orm import Session

engine = None

def connect():
    global engine

    if engine:
        return

    engine = create_engine("mysql+pymysql://Demo:Demo_0000@localhost:3306/MedicationTalk")
    
def get_session():
    if not engine:
        connect()

    return Session(engine)

session = get_session()

@app.route('/api/_add_numbers')
def add_numbers():
    a = request.args.get('a')
    b = request.args.get('b')
    print(a, b)
    result = int(a)+int(b)
    return jsonify(result=result)

@app.route('/api/_patient')
def get_patient_info():
    barcode = request.args.get('barcode')
    sql_cmd = text("""
        select info
        from Patient_Info
        where barcode='{}';
        """.format(barcode))
    
    query_data = session.execute(sql_cmd).fetchall()
    print(query_data)
    if len(query_data) < 1:
        resp = {'info': '查無此病人資料'}
    else:
        resp = {'info': query_data[0][0]}
    
    return jsonify(resp)

@app.route('/api/_level')
def get_level():
    level_num = [0, 0, 0]

    sql_cmd = text("""
        select question_1, question_2, question_3, question_4, question_5, question_6, question_7, question_8, question_9, question_10
        from Record;
        """)
    
    query_data = session.execute(sql_cmd).fetchall()

    for each_record in query_data:
        total_score = sum(each_record)

        if total_score >= 7:
            level_num[2] = level_num[2] + 1
        elif total_score >= 4:
            level_num[1] = level_num[1] + 1
        else: 
            level_num[0] = level_num[0] + 1

    resp = {'level': level_num}
    
    return jsonify(resp)

@app.route('/api/_history')
def get_history():
    user_id = request.args.get('user_id')
    history_data = []
    history_data.clear()
    history_label = []
    history_label.clear()

    sql_cmd = text("""
        select question_1, question_2, question_3, question_4, question_5, question_6, question_7, question_8, question_9, question_10
        from User INNER JOIN Record
        on User.id = Record.user_id
        where student_id='{}';
        """.format(user_id))
    
    query_data = session.execute(sql_cmd).fetchall()
    
    for each_record in query_data:
        total_score = sum(each_record)
        history_data.append(total_score)

    sql_cmd = text("""
        select time
        from User INNER JOIN Record
        on User.id = Record.user_id
        where student_id='{}';
        """.format(user_id))
    
    query_data = session.execute(sql_cmd).fetchall()
    
    for each_record in query_data:
        history_label.append(each_record[0])
                

    resp = {'history_data': history_data,
            'history_label': history_label}
    
    return jsonify(resp)

@app.route('/api/_time_total')
def get_time_total():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    each_q_score = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    sql_cmd = text("""
        select question_1, question_2, question_3, question_4, question_5, question_6, question_7, question_8, question_9, question_10
        from Record
        where time between '{}' and '{}';
        """.format(start_date, end_date))
    
    query_data = session.execute(sql_cmd).fetchall()
    
    for each_record in query_data:
        for i in range(len(each_record)):
            if (each_record[i] == 1):
                each_q_score[i] = each_q_score[i] + 1

            
    resp = {'each_q_score': each_q_score}
    
    return jsonify(resp)

@app.route('/api/_sheet_user', methods=['POST'])
def get_sheet_user():
    sql_cmd = text("""
        select * from User where student_id='{}';
        """.format(request.form['id']))

    sql_result = session.execute(sql_cmd).fetchall()

    if len(sql_result) < 1:
        sql_cmd = text("""
        insert into User (name, student_id)
        values ('{}', '{}')
        """.format(request.form['name'], request.form['id']))

        session.execute(sql_cmd)
        
        session.commit()
    
    return 'ok'



@app.route('/api/_sheet_pill', methods=['POST'])
def get_sheet_pill():
    # pill talbe
    sql_cmd = text("""
        insert into Pill_Medication (pill_name_id, pill_1, pill_2, pill_3, pill_4, pill_5, pill_6, pill_7, pill_8, pill_9) 
        values (1, {}, {}, {}, {}, {}, {}, {}, {}, {});
        """.format(request.form['pills_1'], request.form['pills_2'], request.form['pills_3'], request.form['pills_4'], request.form['pills_5'], request.form['pills_6'], request.form['pills_7'], request.form['pills_8'], request.form['pills_9']))
    
    session.execute(sql_cmd)
    session.commit()
    return 'ok'

@app.route('/api/_sheet_feedback', methods=['POST'])
def get_sheet_feedback():
    # feedback table
    sql_cmd = text("""
        insert into Feedback (question_1, question_2, question_3, question_4, question_5, question_6, question_7, question_8, question_9, question_10) 
        values ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');
        """.format(request.form['reason_1'], request.form['reason_2'], request.form['reason_3'], request.form['reason_4'], request.form['reason_5'], request.form['reason_6'], request.form['reason_7'], request.form['reason_8'], request.form['reason_9'], request.form['reason_10']))

    session.execute(sql_cmd)
    session.commit()
    return 'ok'

@app.route('/api/_sheet_cognition', methods=['POST'])
def get_sheet_cognition():
    # congnition table
    sql_cmd = text("""
        select * from Patient_Info where barcode='{}';
        """.format(request.form['patient_barcode']))

    patient_info_id = session.execute(sql_cmd).fetchall()
    if len(patient_info_id) > 0:
        patient_info_id = patient_info_id[0][0]
    else:
        patient_info_id = -1

    sql_cmd = text("""
        insert into Student_Cognition (patient_info_id, question_1, question_2, question_3, question_4, question_5, question_6, question_7, question_8, question_9, question_10) 
        values ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {});
        """.format(patient_info_id, request.form['student_cognition_1'], request.form['student_cognition_2'], request.form['student_cognition_3'], request.form['student_cognition_4'], request.form['student_cognition_5'], request.form['student_cognition_6'], request.form['student_cognition_7'], request.form['student_cognition_8'], request.form['student_cognition_9'], request.form['student_cognition_10']))

    session.execute(sql_cmd)
    session.commit()

    return 'ok'

@app.route('/api/_sheet_record', methods=['POST'])
def get_sheet_record():
    time.sleep(1)
    # Record table
    sql_cmd = text("""
        SELECT ROW_NUMBER() OVER() AS id FROM Record;
        """)

    rows = len(session.execute(sql_cmd).fetchall())

    sql_cmd = text("""
        select * from User where student_id='{}';
        """.format(request.form['id']))

    user_id = (session.execute(sql_cmd).fetchall())[0][0]
    print(user_id)

    sql_cmd = text("""
        insert into Record (user_id, student_cognition_id, pill_medication_id, feedback_id, question_1, question_2, question_3, question_4, question_5, question_6, question_7, question_8, question_9, question_10, time)
        values ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, now());
        """.format(user_id, rows+1, rows+1, rows+1, request.form['ans_1'], request.form['ans_2'], request.form['ans_3'], request.form['ans_4'], request.form['ans_5'], request.form['ans_6'], request.form['ans_7'], request.form['ans_8'], request.form['ans_9'], request.form['ans_10']))
    session.execute(sql_cmd)
    session.commit()
    return 'ok'

@app.route('/')
def index():

    sql_cmd = text("""
        select *
        from Patient_Info;
        """)
    
    query_data = session.execute(sql_cmd).fetchall()
    print(query_data)
    return 'ok'
 
 
if __name__ == "__main__":
    
    app.run(host='0.0.0.0', port= 7777, ssl_context=('server.crt', 'server.key'))