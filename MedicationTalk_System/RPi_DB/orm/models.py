from sqlalchemy import (Boolean, Column, DateTime, Float, ForeignKey,
                        Integer, String, Text, UniqueConstraint, JSON)
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()

class Patient_Info(base):
    __tablename__ = 'Patient_Info'
    id = Column(Integer, primary_key=True, nullable=False)
    barcode = Column(String(20), nullable=False)
    info = Column(String(200), nullable=False)

class User(base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(20), nullable=False)
    student_id = Column(String(20), nullable=False)

class Pill_Name(base):
    __tablename__ = 'Pill_Name'
    id = Column(Integer, primary_key=True, nullable=False)
    name_1 = Column(String(50), nullable=False)
    name_2 = Column(String(50), nullable=False)
    name_3 = Column(String(50), nullable=False)
    name_4 = Column(String(50), nullable=False)
    name_5 = Column(String(50), nullable=False)
    name_6 = Column(String(50), nullable=False)
    name_7 = Column(String(50), nullable=False)
    name_8 = Column(String(50), nullable=False)
    name_9 = Column(String(50), nullable=False)
    

class Pill_Medication(base):
    __tablename__ = 'Pill_Medication'
    id = Column(Integer, primary_key=True, nullable=False)
    pill_name_id = Column(Integer, ForeignKey('Pill_Name.id'), nullable=False)
    pill_1 = Column(Integer, nullable=False)
    pill_2 = Column(Integer, nullable=False)
    pill_3 = Column(Integer, nullable=False)
    pill_4 = Column(Integer, nullable=False)
    pill_5 = Column(Integer, nullable=False)
    pill_6 = Column(Integer, nullable=False)
    pill_7 = Column(Integer, nullable=False)
    pill_8 = Column(Integer, nullable=False)
    pill_9 = Column(Integer, nullable=False)
    pic = Column(String(20), nullable=False)


class Student_Cognition(base):
    __tablename__ = 'Student_Cognition'
    id = Column(Integer, primary_key=True, nullable=False)
    patient_info_id = Column(Integer, ForeignKey('Patient_Info.id'), nullable=False)
    question_1 = Column(Integer, nullable=False)
    question_2 = Column(Integer, nullable=False)
    question_3 = Column(Integer, nullable=False)
    question_4 = Column(Integer, nullable=False)
    question_5 = Column(Integer, nullable=False)
    question_6 = Column(Integer, nullable=False)
    question_7 = Column(Integer, nullable=False)
    question_8 = Column(Integer, nullable=False)
    question_9 = Column(Integer, nullable=False)
    question_10 = Column(Integer, nullable=False)


class Feedback(base):
    __tablename__ = 'Feedback'
    id = Column(Integer, primary_key=True, nullable=False)
    question_1 = Column(String(50), nullable=False)
    question_2 = Column(String(50), nullable=False)
    question_3 = Column(String(50), nullable=False)
    question_4 = Column(String(50), nullable=False)
    question_5 = Column(String(50), nullable=False)
    question_6 = Column(String(50), nullable=False)
    question_7 = Column(String(50), nullable=False)
    question_8 = Column(String(50), nullable=False)
    question_9 = Column(String(50), nullable=False)
    question_10 = Column(String(50), nullable=False)

class Record(base):
    __tablename__ = 'Record'
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    student_cognition_id = Column(Integer, ForeignKey('Student_Cognition.id'), nullable=False)
    pill_medication_id = Column(Integer, ForeignKey('Pill_Medication.id'), nullable=False)
    feedback_id = Column(Integer, ForeignKey('Feedback.id'), nullable=False)
    question_1 = Column(Integer, nullable=False)
    question_2 = Column(Integer, nullable=False)
    question_3 = Column(Integer, nullable=False)
    question_4 = Column(Integer, nullable=False)
    question_5 = Column(Integer, nullable=False)
    question_6 = Column(Integer, nullable=False)
    question_7 = Column(Integer, nullable=False)
    question_8 = Column(Integer, nullable=False)
    question_9 = Column(Integer, nullable=False)
    question_10 = Column(Integer, nullable=False)
    time = Column(DateTime, nullable=False)
    
class Syringe_Result(base):
    __tablename__ = 'Syringe_Result'
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    lesson = Column(Integer, nullable=False)
    record = Column(JSON, nullable=False)
    time = Column(DateTime, nullable=False)
    
    
