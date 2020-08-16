from datetime import datetime
from StudentCRM import db, LoginManager, app, bcrypt, relationship
from flask_login import UserMixin
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from flask import jsonify, session
import random


@LoginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def whoIs():
    sessions = sessionCheck()

    if 3 in sessions:
        who = 'employer'
    elif 2 in sessions:
        who = 'student'
    elif 1 in sessions:
        who = 'staff'
    else:
        who = ''

    return who

def sessionCheck():
    sessionList = []
    if session.get('user_token'):
        token = str(session.get('user_token'))
        tokenCheckStaff = staff.query.filter_by(token=token).first()
        tokenCheckStudent = students.query.filter_by(token=token, confirm=1).first()
        tokenCheckEmployer = employer.query.filter_by(token=token).first()
        if tokenCheckStaff:
            sessionList.append(1)
        if tokenCheckStudent:
            sessionList.append(2)
        if tokenCheckEmployer:
            sessionList.append(3)
    return sessionList


class staff(db.Model):
    id_staff = db.Column(db.Integer, primary_key=True)
    staff_email = db.Column(db.String(120), unique=True, nullable=False)#Unique=True
    firstName = db.Column(db.String(30), unique=False, nullable=False)
    surname = db.Column(db.String(30), unique=False, nullable=False)
    token = db.Column(db.String(60), unique=True, nullable=True)#Unique=True
    confirm = db.Column(db.Boolean, unique=False, nullable=False)
    signature_image_link = db.Column(db.String(100), unique=False, nullable=True)

    def generate_auth_token(self):
        genToken = bcrypt.generate_password_hash(str(self.staff_email + str(random.getrandbits(128)))).decode('utf-8')
        return genToken


class students(db.Model):
    id_student = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=False, nullable=False)#Unique=True
    firstName = db.Column(db.String(30), unique=False, nullable=False)
    surname = db.Column(db.String(30), unique=False, nullable=False)
    token = db.Column(db.String(60), unique=False, nullable=True)
    nin = db.Column(db.String(6), unique=False, nullable=False)#Unique#True
    date_birth = db.Column(db.DateTime(), unique=False, nullable=False)
    phone = db.Column(db.String(15), unique=False, nullable=False)#Unique=True
    address_1 = db.Column(db.String(40), unique=False, nullable=False)
    address_2 = db.Column(db.String(40), unique=False, nullable=False)
    city = db.Column(db.String(20), unique=False, nullable=False)
    post_code = db.Column(db.String(7), unique=False, nullable=False)
    year_entry = db.Column(db.Integer, unique=False, nullable=False)
    qualification_image_link = db.Column(db.String(100), unique=False, nullable=True)
    address_proof_image_link = db.Column(db.String(100), unique=False, nullable=True)
    signature_image_link = db.Column(db.String(100), unique=False, nullable=True)
    id_image_link = db.Column(db.String(100), unique=False, nullable=True)
    degree_id = db.Column(db.Integer, db.ForeignKey('degree.degree_id'))
    id_staff = db.Column(db.Integer, db.ForeignKey('staff.id_staff'))#Unique=True
    signDate = db.Column(db.DateTime, unique=False, nullable=False)
    confirm = db.Column(db.Boolean, unique=False, nullable=False)
    dataConfirm = db.Column(db.Boolean, unique=False, nullable=False)
    filledIn = db.Column(db.Boolean, unique=False, nullable=True)
    employmentStartDate = db.Column(db.DateTime(), unique=False, nullable=True)
    jobTitle = db.Column(db.String(50), unique=False, nullable=True)
    degree_link = relationship("degree", foreign_keys=[degree_id])

    def generate_auth_token(self):
        genToken = bcrypt.generate_password_hash(str(self.email + str(random.getrandbits(128)))).decode('utf-8')
        return genToken

    def __repr__(self):
        return '{} {}'.format(self.firstName, self.surname)


class achievements(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_student = db.Column(db.Integer, db.ForeignKey('students.id_student'))
    subject = db.Column(db.String(120), unique=False, nullable=False)
    level = db.Column(db.Integer, unique=False, nullable=False)
    grade = db.Column(db.String(3), unique=False, nullable=False)


class verify(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('students.id_student'))
    verifyString = db.Column(db.String(60), unique=True, nullable=True)


class employer(db.Model):
    id_employer = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(30), unique=False, nullable=False)
    surname = db.Column(db.String(30), unique=False, nullable=False)
    employer_email = db.Column(db.String(120), unique=False, nullable=False)#Unique=True
    token = db.Column(db.String(60), unique=False, nullable=True)#Unique=True
    address_1 = db.Column(db.String(40), unique=False, nullable=False)
    address_2 = db.Column(db.String(40), unique=False, nullable=False)
    city = db.Column(db.String(20), unique=False, nullable=False)
    post_code = db.Column(db.String(7), unique=False, nullable=False)
    id_student = db.Column(db.Integer, db.ForeignKey('students.id_student'))
    confirm = db.Column(db.Boolean, unique=False, nullable=False)
    signature_image_link = db.Column(db.String(100), unique=False, nullable=True)

    def generate_auth_token(self):
        genToken = bcrypt.generate_password_hash(str(self.employer_email + str(random.getrandbits(128)))).decode('utf-8')
        return genToken


class progress_report(db.Model):
    progress_report_id = db.Column(db.Integer, primary_key=True)
    id_staff_writer = db.Column(db.Integer, db.ForeignKey('staff.id_staff'))
    id_employer_writer = db.Column(db.Integer, db.ForeignKey('employer.id_employer'))
    id_student = db.Column(db.Integer, db.ForeignKey('students.id_student'))
    year = db.Column(db.Integer, unique=False, nullable=False)
    course_name = db.Column(db.String(50), unique=False, nullable=False)
    question_1 = db.Column(db.String, unique=False, nullable=False)
    question_2 = db.Column(db.String, unique=False, nullable=False)
    question_3 = db.Column(db.String, unique=False, nullable=True)


class degree(db.Model):
    degree_id = db.Column(db.Integer, primary_key=True)
    degree_name = db.Column(db.String(50), unique=False, nullable=False)
    length = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return '{}'.format(self.degree_name)

class apprenticeship_evaluation(db.Model):
    report_id = db.Column(db.Integer, primary_key=True)
    id_student = db.Column(db.Integer, db.ForeignKey('students.id_student'), unique=False, nullable=False) #Unique=True
    overall_exp = db.Column(db.Integer, unique=False, nullable=False)
    year = db.Column(db.Integer, unique=False, nullable=False)
    q_1 = db.Column(db.Integer, unique=False, nullable=False)
    c_1 = db.Column(db.String, unique=False, nullable=False)
    q_2 = db.Column(db.Integer, unique=False, nullable=False)
    c_2 = db.Column(db.String, unique=False, nullable=False)
    q_3 = db.Column(db.Integer, unique=False, nullable=False)
    c_3 = db.Column(db.String, unique=False, nullable=False)
    q_4 = db.Column(db.Integer, unique=False, nullable=False)
    c_4 = db.Column(db.String, unique=False, nullable=False)
    q_5 = db.Column(db.Integer, unique=False, nullable=False)
    c_5 = db.Column(db.String, unique=False, nullable=False)
    q_6 = db.Column(db.Integer, unique=False, nullable=False)
    c_6 = db.Column(db.String, unique=False, nullable=False)
    q_7 = db.Column(db.Integer, unique=False, nullable=False)
    c_7 = db.Column(db.String, unique=False, nullable=False)
    q_8 = db.Column(db.Integer, unique=False, nullable=False)
    c_8 = db.Column(db.String, unique=False, nullable=False)
    q_9 = db.Column(db.Integer, unique=False, nullable=False)
    c_9 = db.Column(db.String, unique=False, nullable=False)
    q_10 = db.Column(db.Integer, unique=False, nullable=False)
    c_10 = db.Column(db.String, unique=False, nullable=False)

class equality_monitoring(db.Model):
    equality_id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, unique=False)
    degree_id = db.Column(db.Integer, unique=False, nullable=False)
    ethnic_group = db.Column(db.Integer, unique=False, nullable=False)
    religion_group = db.Column(db.Integer, unique=False, nullable=False)
    transgender = db.Column(db.Integer, unique=False, nullable=False)
    sexual_orientation = db.Column(db.Integer, unique=False, nullable=False)
    care_experience = db.Column(db.Integer, unique=False, nullable=False)
    gender = db.Column(db.Integer, unique=False, nullable=False)
    disability = db.Column(db.Integer, unique=False, nullable=False)
    illness_asperger = db.Column(db.Boolean, unique=False, nullable=False)
    illness_blind = db.Column(db.Boolean, unique=False, nullable=False)
    illness_deaf = db.Column(db.Boolean, unique=False, nullable=False)
    illness_long = db.Column(db.Boolean, unique=False, nullable=False)
    illness_mental = db.Column(db.Boolean, unique=False, nullable=False)
    illness_learning = db.Column(db.Boolean, unique=False, nullable=False)
    illness_mobility = db.Column(db.Boolean, unique=False, nullable=False)
    illness_not_listed = db.Column(db.Boolean, unique=False, nullable=False)
    illness_not_to_say = db.Column(db.Boolean, unique=False, nullable=False)
