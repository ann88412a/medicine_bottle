from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_cors import CORS
import time
import datetime



app = Flask(__name__, template_folder="templates", static_folder='static',)
# CORS(app, resources={r"/api/*": {"origins": ["https://ann88412a.github.io", "140.113.*.*"]}}) 
# CORS(app, resources={r"/api/*": {"origins": ["0.0.0.0", "*.*.*.*"]}}) 
# app.config['PROPAGATE_EXCEPTIONS'] = False
CORS(app, resources={r"/api/*": {"origins": ["*"]}})

from sqlalchemy import create_engine, text, or_
from sqlalchemy.orm import Session
import models


engine = None

def connect():
    global engine

    if engine:
        return

    engine = create_engine("mysql+pymysql://Demo:Demo_0000@localhost:3306/MedicationTalk")
    
    models.base.metadata.create_all(engine)

def get_session():
    if not engine:
        connect()

    return Session(engine)

session = get_session()

# @app.route("/index") 
# def hello(): 
#     return render_template('index.html') 

@app.route('/api/_patient')
def get_patient_info():
    barcode = request.args.get('barcode')
    result = session.query(models.Patient_Info).filter(models.Patient_Info.barcode == barcode).first()
    if result == None:
        resp = {'info': '查無此病人資料'}
    else:
        resp = {'info': result.info}
    # sql_cmd = text("""
    #     select info
    #     from Patient_Info
    #     where barcode='{}';
    #     """.format(barcode))
    
    # query_data = session.execute(sql_cmd).fetchall()
    # print(query_data)
    # if len(query_data) < 1:
    #     resp = {'info': '查無此病人資料'}
    # else:
    #     resp = {'info': query_data[0][0]}
    
    return jsonify(resp)

@app.route('/api/_level')
def get_level():
    level_num = [0, 0, 0]
    result = session.query(models.Record).all()

    for each_record in result:
        total_score = each_record.question_1 + each_record.question_2 + each_record.question_3 + each_record.question_4 + each_record.question_5 + each_record.question_6 + each_record.question_7 + each_record.question_8 + each_record.question_9 + each_record.question_10
        if total_score >= 7:
            level_num[2] = level_num[2] + 1
        elif total_score >= 4:
            level_num[1] = level_num[1] + 1
        else: 
            level_num[0] = level_num[0] + 1
    # sql_cmd = text("""
    #     select question_1, question_2, question_3, question_4, question_5, question_6, question_7, question_8, question_9, question_10
    #     from Record;
    #     """)
    
    # query_data = session.execute(sql_cmd).fetchall()

    # for each_record in query_data:
    #     total_score = sum(each_record)

        # if total_score >= 7:
        #     level_num[2] = level_num[2] + 1
        # elif total_score >= 4:
        #     level_num[1] = level_num[1] + 1
        # else: 
        #     level_num[0] = level_num[0] + 1

    resp = {'level': level_num}
    
    return jsonify(resp)

@app.route('/api/_history')
def get_history():
    user_id = request.args.get('user_id')
    history_data = []
    history_data.clear()
    history_label = []
    history_label.clear()

    # result = session.query(models.User).join(models.Record).filter_by(student_id = user_id).all()
    
    # for each_record in result:
    #     total_score = each_record.question_1 + each_record.question_2 + each_record.question_3 + each_record.question_4 + each_record.question_5 + each_record.question_6 + each_record.question_7 + each_record.question_8 + each_record.question_9 + each_record.question_10
    #     history_data.append(total_score)
    #     history_label.append(each_record.time)
    
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

    # result = session.query(models.Record).filter(models.Record.time >= start_date and models.Record.time <= end_date).all()
        
    # for each_record in result:
    #     if each_record.question_1 == 1:
    #         each_q_score[0] = each_q_score[0] + 1
    #     if each_record.question_2 == 1:
    #         each_q_score[1] = each_q_score[1] + 1
    #     if each_record.question_3 == 1:
    #         each_q_score[2] = each_q_score[2] + 1
    #     if each_record.question_4 == 1:
    #         each_q_score[3] = each_q_score[3] + 1
    #     if each_record.question_5 == 1:
    #         each_q_score[4] = each_q_score[4] + 1
    #     if each_record.question_6 == 1:
    #         each_q_score[5] = each_q_score[5] + 1
    #     if each_record.question_7 == 1:
    #         each_q_score[6] = each_q_score[6] + 1
    #     if each_record.question_8 == 1:
    #         each_q_score[7] = each_q_score[7] + 1
    #     if each_record.question_9 == 1:
    #         each_q_score[8] = each_q_score[8] + 1
    #     if each_record.question_10 == 1:
    #         each_q_score[9] = each_q_score[9] + 1
            
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
    user_data =  request.form 
   
    user_result = session.query(models.User).filter(models.User.student_id == user_data['id']).count()
    print(user_result)
    if user_result < 1:
        insert_value = models.User(name = user_data['name'], student_id = user_data['id'])
        session.add(insert_value)
        session.commit()

    # sql_cmd = text("""
    #     select * from User where student_id='{}';
    #     """.format(request.form['id']))

    # sql_result = session.execute(sql_cmd).fetchall()

    # if len(sql_result) < 1:
    #     sql_cmd = text("""
    #     insert into User (name, student_id)
    #     values ('{}', '{}')
    #     """.format(request.form['name'], request.form['id']))

    #     session.execute(sql_cmd)
        
    #     session.commit()
    
    return 'ok'



@app.route('/api/_sheet_pill', methods=['POST'])
def get_sheet_pill():
    # pill talbe
    
    pill_data =  request.form 
    print('pill-------', pill_data)
    insert_pill = models.Pill_Medication(pill_name_id = int(pill_data['pill_name_id']), pill_1 = int(pill_data['pills_1']), pill_2 = int(pill_data['pills_2']), pill_3 = int(pill_data['pills_3']), pill_4 = int(pill_data['pills_4']), pill_5 = int(pill_data['pills_5']), pill_6 = int(pill_data['pills_6']), pill_7 = int(pill_data['pills_7']), pill_8 = int(pill_data['pills_8']), pill_9 = int(pill_data['pills_9']), pic = pill_data['pic'] )
    session.add(insert_pill)
    
    # sql_cmd = text("""
    #     insert into Pill_Medication (pill_name_id, pill_1, pill_2, pill_3, pill_4, pill_5, pill_6, pill_7, pill_8, pill_9, pic) 
    #     values (1, {}, {}, {}, {}, {}, {}, {}, {}, {}, {});
    #     """.format(request.form['pills_1'], request.form['pills_2'], request.form['pills_3'], request.form['pills_4'], request.form['pills_5'], request.form['pills_6'], request.form['pills_7'], request.form['pills_8'], request.form['pills_9']), request.form['pic'])
    
    # session.execute(sql_cmd)
    session.commit()
    return 'ok'
    

@app.route('/api/_sheet_syringe', methods=['POST'])
def get_sheet_syringe():
    # syringe table
    
    # sql_cmd = text("""
    #     select * from Patient_Info where barcode='{}';
    #     """.format(request.form['patient_barcode']))

    # patient_info_id = session.execute(sql_cmd).fetchall()
    # if len(patient_info_id) > 0:
    #     patient_info_id = patient_info_id[0][0]
    # else:
    #     patient_info_id = -1
        
    # sql_cmd = text("""
    #     insert into Syringe_Result (user_id, lesson, record) 
    #     values ({}, {}, {});
    #     """.format(patient_info_id, 1, {'test':1}))
    
    # session.execute(sql_cmd)
    # session.commit()
    return 'ok'
    

@app.route('/api/_sheet_feedback', methods=['POST'])
def get_sheet_feedback():
    # feedback table
    
    feedback_data =  request.form 
    print('feedback-------', feedback_data)
    insert_feedback = models.Feedback(question_1 = feedback_data['reason_1'], question_2 = feedback_data['reason_2'], question_3 = feedback_data['reason_3'], question_4 = feedback_data['reason_4'], question_5 = feedback_data['reason_5'], question_6 = feedback_data['reason_6'], question_7 = feedback_data['reason_7'], question_8 = feedback_data['reason_8'], question_9 = feedback_data['reason_9'], question_10 = feedback_data['reason_10'] )
    session.add(insert_feedback)
    
    # sql_cmd = text("""
    #     insert into Feedback (question_1, question_2, question_3, question_4, question_5, question_6, question_7, question_8, question_9, question_10) 
    #     values ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');
    #     """.format(request.form['reason_1'], request.form['reason_2'], request.form['reason_3'], request.form['reason_4'], request.form['reason_5'], request.form['reason_6'], request.form['reason_7'], request.form['reason_8'], request.form['reason_9'], request.form['reason_10']))

    # session.execute(sql_cmd)
    session.commit()
    return 'ok'

@app.route('/api/_sheet_cognition', methods=['POST'])
def get_sheet_cognition():
    # congnition table
    congnition_data =  request.form 
    print('congnition-------', congnition_data)
    
    sql_cmd = text("""
        select * from Patient_Info where barcode='{}';
        """.format(congnition_data['patient_barcode']))

    patient_info_id = session.execute(sql_cmd).fetchall()
    print(patient_info_id)
    if len(patient_info_id) > 0:
        patient_info_id = patient_info_id[0][0]
    else:
        patient_info_id = -1

    insert_congnition = models.Student_Cognition(question_1 = int(congnition_data['student_cognition_1']), question_2 = int(congnition_data['student_cognition_2']), question_3 = int(congnition_data['student_cognition_3']), question_4 = int(congnition_data['student_cognition_4']), question_5 = int(congnition_data['student_cognition_5']), question_6 = int(congnition_data['student_cognition_6']), question_7 = int(congnition_data['student_cognition_7']), question_8 = int(congnition_data['student_cognition_8']), question_9 = int(congnition_data['student_cognition_9']), question_10 = int(congnition_data['student_cognition_10']) )
    session.add(insert_congnition)
    session.commit()

    # sql_cmd = text("""
    #     insert into Student_Cognition (patient_info_id, question_1, question_2, question_3, question_4, question_5, question_6, question_7, question_8, question_9, question_10) 
    #     values ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {});
    #     """.format(patient_info_id, request.form['student_cognition_1'], request.form['student_cognition_2'], request.form['student_cognition_3'], request.form['student_cognition_4'], request.form['student_cognition_5'], request.form['student_cognition_6'], request.form['student_cognition_7'], request.form['student_cognition_8'], request.form['student_cognition_9'], request.form['student_cognition_10']))

    # session.execute(sql_cmd)
    # session.commit()

    return 'ok'

@app.route('/api/_sheet_record', methods=['POST'])
def get_sheet_record():
    # time.sleep(1)
    # # Record table
    record_data = request.form

    sql_cmd = text("""
    select * from User where student_id='{}';
    """.format(request.form['id']))

    user_table_id = (session.execute(sql_cmd).fetchall())[0][0]
    print(user_table_id)
    

    sql_cmd = text("""
        SELECT * FROM Student_Cognition;
        """)
 
    cognition_rows = session.execute(sql_cmd).fetchall()[-1][0]
    print(cognition_rows)

    sql_cmd = text("""
        SELECT * FROM Pill_Medication;
        """)
 
    pill_rows = session.execute(sql_cmd).fetchall()[-1][0]
    print(pill_rows)

    sql_cmd = text("""
        SELECT * FROM Feedback;
        """)
 
    feedback_rows = session.execute(sql_cmd).fetchall()[-1][0]
    print(feedback_rows)

    now = datetime.datetime.now()
    now = now.strftime('%Y-%m-%d-%H-%M-%S')

    # insert_record = models.Record(user_id = int(user_table_id), student_cognition_id = int(cognition_rows), pill_medication_id = int(pill_rows), feedback_id = int(feedback_rows), question_1 = int(record_data['ans_1']), question_2 = int(record_data['ans_2']), question_3 = int(record_data['ans_3']), question_4 = int(record_data['ans_4']), question_5 = int(record_data['ans_5']), question_6 = int(record_data['ans_6']), question_7 = int(record_data['ans_7']), question_8 = int(record_data['ans_8']), question_9 = int(record_data['ans_9']), question_10 = int(record_data['ans_10']), time = now )
    # session.add(insert_record)
    # session.commit()

    sql_cmd = text("""
        insert into Record (user_id, student_cognition_id, pill_medication_id, feedback_id, question_1, question_2, question_3, question_4, question_5, question_6, question_7, question_8, question_9, question_10, time)
        values ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, now());
        """.format(int(user_table_id), cognition_rows, pill_rows, feedback_rows, record_data['ans_1'], record_data['ans_2'], record_data['ans_3'], record_data['ans_4'], record_data['ans_5'], record_data['ans_6'], record_data['ans_7'], record_data['ans_8'], record_data['ans_9'], record_data['ans_10']))
    session.execute(sql_cmd)
    session.commit()
    return 'ok'

@app.route('/api/_pic', methods=['POST'])
def get_pic():
    file = request.files['file']
    
    file.save('./backup/' + request.form['name'] + '.jpg')
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
    
    app.run(host='0.0.0.0', port= 15260, debug=True)# , ssl_context=('server.crt', 'server.key')
