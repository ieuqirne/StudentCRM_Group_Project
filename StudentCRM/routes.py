from flask import render_template, url_for, flash, redirect, request, session
from StudentCRM.forms import RegistrationForm, LoginForm, EqualityForm,EmployerProgressForm,StudentProgressForm,\
    StaffProgressForm, StudentEvaluationForm, CreateStaff, TestFileUpload, EditProfileForm, UploadSignature
from StudentCRM.models import students, employer, degree, equality_monitoring, progress_report, \
    apprenticeship_evaluation, staff, achievements, sessionCheck, whoIs, verify
from StudentCRM import app, db, bcrypt, mysql, ALLOWED_EXTENSIONS, mail, Message, Mail, UPLOAD_FOLDER
from flask_login import login_user, current_user, logout_user, login_required
import random, os, hashlib
from datetime import datetime, timedelta, date
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from werkzeug.utils import secure_filename
from flask import Markup


@app.route("/")
@app.route("/Home")
@app.route("/home")
def home():
    sessions = sessionCheck()
    whos = whoIs()
    print(UPLOAD_FOLDER)
    pageTitle = "Become an Apprentice"
    return render_template('index.html', pageTitle=pageTitle, whos=whos)


@app.route("/about")
def about():
    whos = whoIs()
    return render_template('about.html', whos=whos)


@app.route("/privacy")
def privacy():
    whos = whoIs()
    return render_template('privacy_statement.html', whos=whos)

@app.errorhandler(404)
def page_not_found(error):
    whos = whoIs()
    pageTitle = "404 - Page Not Found"
    return render_template('404.html', pageTitle=pageTitle, whos=whos), 404


@app.route('/confirmStudent')
@app.route('/ConfirmStudent')
def confirmStudent():
    sessions = sessionCheck()
    whos = whoIs()
    if 1 in sessions:
        print('SessionValid')
    else:
        return redirect(url_for('login'))
    studentId = request.args.get('ID')
    getStudent = students.query.filter_by(id_student=studentId).first()
    getStudent.dataConfirm = True
    db.session.commit()
    return redirect('/adminView?ID='+studentId)


@app.route("/AdminDash", methods=['GET', 'POST'])
@app.route("/adminDash", methods=['GET', 'POST'])
def adminDash():
    sessions = sessionCheck()
    whos = whoIs()
    if 1 in sessions:
        print('SessionValid')
    else:
        return redirect(url_for('login'))
    Students = students.query.all()
    return render_template('adminDashboard.html', Students=Students, whos=whos)


@app.route("/equalitystats/<int:year>", methods=['GET', 'POST'])
@app.route("/equalityStats/<int:year>", methods=['GET', 'POST'])
def equalitystats(year=None):
    sessions = sessionCheck()
    whos = whoIs()
    if 1 in sessions:
        print('SessionValid')
    else:
        return redirect(url_for('login'))

    degree = []
    for x in range(1, 14):
        degree.append(equality_monitoring.query.filter_by(degree_id=x, year=year).count())
    ethnic = []
    for x in range(1, 17):
        ethnic.append(equality_monitoring.query.filter_by(ethnic_group=x, year=year).count())
    religion = []
    for x in range(1, 13):
        religion.append(equality_monitoring.query.filter_by(religion_group=x, year=year).count())
    transgender = []
    for x in range(1, 4):
        transgender.append(equality_monitoring.query.filter_by(transgender=x, year=year).count())
    sexual_orientation = []
    for x in range(1, 6):
        sexual_orientation.append(equality_monitoring.query.filter_by(sexual_orientation=x, year=year).count())
    care_experience = []
    for x in range(1, 4):
        care_experience.append(equality_monitoring.query.filter_by(care_experience=x, year=year).count())
    gender = []
    for x in range(1, 3):
        gender.append(equality_monitoring.query.filter_by(gender=x, year=year).count())
    disability = []
    for x in range(1, 4):
        disability.append(equality_monitoring.query.filter_by(disability=x, year=year).count())

    otherDis = []
    otherDis.append(equality_monitoring.query.filter_by(illness_asperger=1, year=year).count())
    otherDis.append(equality_monitoring.query.filter_by(illness_blind=1, year=year).count())
    otherDis.append(equality_monitoring.query.filter_by(illness_deaf=1, year=year).count())
    otherDis.append(equality_monitoring.query.filter_by(illness_long=1, year=year).count())
    otherDis.append(equality_monitoring.query.filter_by(illness_mental=1, year=year).count())
    otherDis.append(equality_monitoring.query.filter_by(illness_learning=1, year=year).count())
    otherDis.append(equality_monitoring.query.filter_by(illness_mobility=1, year=year).count())
    otherDis.append(equality_monitoring.query.filter_by(illness_not_listed=1, year=year).count())
    otherDis.append(equality_monitoring.query.filter_by(illness_not_to_say=1, year=year).count())

    year = datetime.utcnow().year
    years = []
    for x in range(2015, (year + 1)):
        total = equality_monitoring.query.filter_by(year=x).count()
        if total > 0:
            years.append(x)
    print(years)

    print(otherDis)

    return render_template('equalityStats.html', degree=degree, ethnic=ethnic, religion=religion,
                           transgender=transgender, sexual_orientation=sexual_orientation,
                           care_experience=care_experience, gender=gender,
                           disability=disability, otherDis=otherDis, years=years, whos=whos, year=year)


@app.route("/sendReminder", methods=['GET', 'POST'])
@app.route("/SendReminder", methods=['GET', 'POST'])
def sendReminder():
    sessions = sessionCheck()
    whos = whoIs()
    if 1 in sessions:
        print('SessionValid')
    else:
        return redirect(url_for('login'))

    reminderType = request.args.get('ReminderType')
    print(reminderType)
    studentEmail = request.args.get('StudentEmail')
    print(studentEmail)
    return redirect(url_for('adminDash'))


@app.route("/editDetails", methods=['GET', 'POST'])
@app.route("/EditDetails", methods=['GET, POST'])
def editDetails():
    sessions = sessionCheck()
    whos = whoIs()
    if 1 in sessions:
        print("SessionValid")
    else:
        return redirect(url_for('login'))
    studentIDForQuery = request.args.get('ID')

    if studentIDForQuery == None:
        return  redirect(url_for('adminDash'))

    studentInfo = students.query.filter_by(id_student=studentIDForQuery).first()

    student = students.query.get_or_404(studentInfo.id_student)
    if studentInfo:
        print('UserFound')
    else:
        print('UserNotFound')
        return redirect(url_for('adminDash'))

    employerInfo = employer.query.filter_by(id_student=studentIDForQuery).first()

    if employerInfo:
        print('EmployerFound')
    else:
        print('EmployerNotFound')
        return redirect(url_for('adminDash'))

    achievementsInfo = achievements.query.filter_by(id_student=studentIDForQuery).all()

    subject = []
    level = []
    grade = []

    for achi in achievementsInfo:
        subject.append(achi.subject)
        level.append(achi.level)
        grade.append(achi.grade)

    if achievementsInfo:
        print('AchievementsFound')
    else:
        print('AchievementsNotFound')
    form = EditProfileForm()
    if form.validate_on_submit():
        student.nin = form.NationalInsurance.data
        student.email = form.emailAddress.data
        student.firstName = form.firstName.data
        student.surname = form.lastName.data
        student.date_birth = form.dateOfBirth.data
        student.phone = form.contactNumber.data
        student.address_1 = form.fLineAddress.data
        student.address_2 = form.sLineAddress.data
        student.city = form.townCity.data
        student.post_code = form.postcode.data
        student.year_entry = form.entryLevel.data
        student.degree_id = form.selectCourse.data.degree_id
        student.employmentStartDate = form.employmentStartDate.data
        student.jobTitle = form.jobTitle.data
        employerInfo.firstName = form.employerFirstName.data
        employerInfo.surname = form.employerSurname.data
        employerInfo.employer_email = form.employerEmail.data
        employerInfo.address_1 = form.employerFAddress.data
        employerInfo.address_2 = form.employerSAddress.data
        employerInfo.city = form.employerTownCity.data
        employerInfo.post_code = form.employerPostcode.data

        subjectInfo = []
        levelInfo = []
        gradeInfo = []
        subjectInfo.append(form.subjectOne.data)
        levelInfo.append(form.levelOne.data)
        gradeInfo.append(form.gradeOne.data)

        subjectInfo.append(form.subjectTwo.data)
        levelInfo.append(form.levelTwo.data)
        gradeInfo.append(form.gradeTwo.data)

        subjectInfo.append(form.subjectThree.data)
        levelInfo.append(form.levelThree.data)
        gradeInfo.append(form.gradeThree.data)

        subjectInfo.append(form.subjectFour.data)
        levelInfo.append(form.levelFour.data)
        gradeInfo.append(form.gradeFour.data)

        subjectInfo.append(form.subjectFive.data)
        levelInfo.append(form.levelFive.data)
        gradeInfo.append(form.gradeFive.data)

        subjectInfo.append(form.subjectSix.data)
        levelInfo.append(form.levelSix.data)
        gradeInfo.append(form.gradeSix.data)

        subjectInfo.append(form.subjectSeven.data)
        levelInfo.append(form.levelSeven.data)
        gradeInfo.append(form.gradeSeven.data)

        subjectInfo.append(form.subjectEight.data)
        levelInfo.append(form.levelEight.data)
        gradeInfo.append(form.gradeEight.data)
        print("subject info len")
        print(len(subjectInfo))
        for x in range(0, 8):
            if x < len(subject):
                if subjectInfo[x]:
                    print("achievements inforasdfasdfasdfasdfasdfsd")
                    print(achievementsInfo[x].id)
                    achiev = achievements.query.filter_by(id=achievementsInfo[x].id).first()
                    print(achiev)
                    achiev.subject = subjectInfo[x]
                    achiev.level = levelInfo[x]
                    achiev.grade = gradeInfo[x]
                    db.session.add(achiev)
                    db.session.commit()
                    print('Added')

        db.session.add(student)
        db.session.add(employerInfo)
        db.session.commit()
        flash('Thanks for Editing details')
        return redirect(url_for('login'))
    else:
        print("here")
        print(form.errors)
        return render_template('editDetails.html', form=form, studentInfo=studentInfo, employerInfo=employerInfo,
                           achievementsInfo=achievementsInfo, whos=whos, subject=subject, level=level, grade=grade)


@app.route('/DeleteRecord', methods=['GET', 'POST'])
def deleteRec():
    sessions = sessionCheck()
    if 1 in sessions:
        print('Session Valid')
    else:
        return redirect(url_for('login'))

    studentIDForQuery = request.args.get('ID')

    if studentIDForQuery:
        print('ID RECIEVED')
    else:
        print('NO ID RECIEVED')
        return redirect(url_for('adminDash'))
    getStudent = students.query.filter_by(id_student=studentIDForQuery).first()
    if getStudent:
        print('Student Found')
    else:
        print('Student NOT FOUND')
        return redirect(url_for('adminDash'))
    getEval = apprenticeship_evaluation.query.filter_by(id_student=studentIDForQuery).all()
    ids = []
    for eval in getEval:
        ids.append(eval.report_id)

    if len(getEval) > 0:
        for x in range(0,len(ids)):
            delQuery = apprenticeship_evaluation.query.filter_by(report_id=ids[x]).first()
            db.session.delete(delQuery)
            db.session.commit()

    ids = []
    getAchiv = achievements.query.filter_by(id_student=studentIDForQuery).all()
    for achi in getAchiv:
        ids.append(achi.id)
    print("lens id")
    print(len(ids))
    progressReports = progress_report.query.filter_by(id_student=getStudent.id_student).all()
    ids = []
    for pro in progressReports:
        ids.append(pro.progress_report_id)
    if len(progressReports) > 0:
        for x in range(0,len(ids)):
            delQuery = progress_report.query.filter_by(progress_report_id=ids[x]).first()
            db.session.delete(delQuery)
            db.session.commit()

    for x in range(0, len(ids)):
        achiev = achievements.query.filter_by(id=ids[x]).first()
        db.session.delete(achiev)
        db.session.commit()
        print('DELETED')

    if getAchiv:
        print('Achiv Found')
    else:
        print('No Achiv Found')
    getEmployer = employer.query.filter_by(id_student=studentIDForQuery).first()
    if getEmployer:
        print('Employer Found')
    else:
        print('No Employer Found')
    if getEmployer:
        db.session.delete(getEmployer)
        db.session.commit()
    else:
        print('No Employer')
    db.session.delete(getStudent)
    db.session.commit()
    flash('Deleted Student ' + studentIDForQuery)
    return redirect(url_for('adminDash'))


@app.route('/RemindStudentEquality', methods=['GET', 'POST'])
@app.route('/remindStudentEquality', methods=['GET', 'POST'])
def remindEquality():
    sessions = sessionCheck()
    if 1 in sessions:
        print('SessionValid')
    else:
        return redirect(url_for('login'))
    studentIDForQuery = request.args.get('ID')
    if studentIDForQuery == None:
        return redirect(url_for('adminDash'))

    studentInfo = students.query.filter_by(id_student=studentIDForQuery).first()

    if studentInfo:
        print('UserFound')
    else:
        print('User not found')

    reminderType = 'Equality Form'

    msg = Message('REMINDER', sender='studentcrmemail@gmail.com',
                  recipients=['studentcrmemail@gmail.com'])

    msg.html = render_template('emailRemind.html', reminderType=reminderType, studentInfo=studentInfo)
    mail.send(msg)
    flash('Reminder Sent')
    return redirect(url_for('adminDash'))


@app.route('/RemindStudentProgress', methods=['GET', 'POST'])
@app.route('/remindStudentProgress', methods=['GET', 'POST'])
def remindProgress():
    sessions = sessionCheck()
    if 1 in sessions:
        print('SessionValid')
    else:
        return redirect(url_for('login'))

    studentIDForQuery = request.args.get('ID')

    if studentIDForQuery == None:
        return redirect(url_for('adminDash'))

    studentInfo = students.query.filter_by(id_student=studentIDForQuery).first()

    if studentInfo:
        print('UserFound')
    else:
        print('User not found')

    reminderType = 'Progress Report'

    msg = Message('REMINDER', sender='studentcrmemail@gmail.com',
                  recipients=['studentcrmemail@gmail.com'])

    msg.html = render_template('emailRemind.html', reminderType=reminderType, studentInfo=studentInfo)
    mail.send(msg)
    flash('Reminder Sent')
    return redirect(url_for('adminDash'))


@app.route('/RemindStudentEvaluation', methods=['GET', 'POST'])
@app.route('/remindStudentEvaluation', methods=['GET', 'POST'])
def remindEval():
    sessions = sessionCheck()
    if 1 in sessions:
        print('SessionValid')
    else:
        return redirect(url_for('login'))

    studentIDForQuery = request.args.get('ID')

    if studentIDForQuery == None:
        return redirect(url_for('adminDash'))

    studentInfo = students.query.filter_by(id_student=studentIDForQuery).first()

    if studentInfo:
        print('UserFound')
    else:
        print('User not found')

    reminderType = 'Evaluation Form'

    msg = Message('REMINDER', sender='studentcrmemail@gmail.com',
                  recipients=['studentcrmemail@gmail.com'])

    msg.html = render_template('emailRemind.html', reminderType=reminderType, studentInfo=studentInfo)
    mail.send(msg)
    flash('Reminder Sent')
    return redirect(url_for('adminDash'))


@app.route("/adminView", methods=['GET', 'POST'])
@app.route("/AdminView", methods=['GET', 'POST'])
def adminView():
    sessions = sessionCheck()
    whos = whoIs()
    if 1 in sessions:
        print('SessionValid')
    else:
        return redirect(url_for('login'))

    studentIDForQuery = request.args.get('ID')

    if studentIDForQuery == None:
        return redirect(url_for('adminDash'))

    studentInfo = students.query.filter_by(id_student=studentIDForQuery).first()

    if studentInfo:
        print('UserFound')
    else:
        print('User not found')
        return redirect(url_for('adminDash'))

    regCompleteQuery = students.query.filter_by(id_student=studentIDForQuery).first()

    if regCompleteQuery:
        regComplete = 'Complete'
    else:
        regComplete = 'Incomplete'

    if regCompleteQuery.filledIn == 1:
        equalityComplete = 'Complete'
    else:
        equalityComplete = 'Incomplete'

    progCompleteQuery = progress_report.query.filter_by(id_student=studentIDForQuery).first()

    if progCompleteQuery:
        progComplete = 'Complete'
    else:
        progComplete = 'Incomplete'

    appEvalCompleteQuery = apprenticeship_evaluation.query.filter_by(id_student=studentIDForQuery).first()

    if appEvalCompleteQuery:
        evalComplete = 'Complete'
    else:
        evalComplete = 'Incomplete'

    checkRegConfirm = students.query.filter_by(id_student=studentIDForQuery).first()
    if checkRegConfirm.dataConfirm == 1:
        dataConfirmed = 'Confirmed'
    else:
        dataConfirmed = 'Not Confirmed'

    return render_template('adminView.html', studentInfo=studentInfo, regComplete=regComplete,
                           equalityComplete=equalityComplete, progComplete=progComplete, evalComplete=evalComplete,
                           dataConfirmed=dataConfirmed, whos=whos)


@app.route("/testUpload", methods=['GET', 'POST'])
def testUpload():
    form = TestFileUpload()
    whos = whoIs()
    if request.method == 'POST':
        uploaded_files1 = request.files.get('file1')
        if uploaded_files1:
            filename = secure_filename(uploaded_files1.filename)
            filename = filename.split('.')
            if filename[1] in ALLOWED_EXTENSIONS:
                hashFile = hashlib.md5(str(filename[0] + str(random.getrandbits(64))).encode()).hexdigest()
                filename = hashFile + '.' + filename[1]
                print(filename)
                uploaded_files1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        uploaded_files2 = request.files.get('file2')
        uploaded_files3 = request.files.get('file3')
        print(uploaded_files1)
        print(uploaded_files2)
        print(uploaded_files3)

    return render_template('uploadTest.html', form=form, whos=whos)


def validate_email(emailAddress):
    emailCheckStudent = students.query.filter_by(email=emailAddress).first()
    emailCheckEmployer = employer.query.filter_by(employer_email=emailAddress).first()
    emailCheckStaff = staff.query.filter_by(staff_email=emailAddress).first()
    if emailCheckStudent or emailCheckStaff or emailCheckEmployer:
        print('Email Already Exists in our database.')
        return False
    else:
        return True

@app.route('/register', methods=['GET', 'POST'])
@app.route('/Register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    whos = whoIs()
    pageTitle = "Register"
    # ACHIEVEMENTS NEED ADDED
    if form.validate_on_submit():
        form.hidden_tag()
        checkEmail = validate_email(form.emailAddress.data)
        if checkEmail == False:
            flash('Email Already Exists In Our Database.')
            return redirect(url_for('register'))
        if request.method == "POST":
            qualUploadImage = request.files.get('qualificationProofImage')
            addressProof = request.files.get('addressProofImage')
            appSigImage = request.files.get('apprenticeSignature')
            idProof = request.files.get('idProofImage')
            print(qualUploadImage)
            print(addressProof)
            print(appSigImage)
            print(idProof)
            if idProof:
                filename = secure_filename(idProof.filename)
                filename = filename.split('.')
                if filename[1] in ALLOWED_EXTENSIONS:
                    hashFile = hashlib.md5(str(filename[0] + str(random.getrandbits(64))).encode()).hexdigest()
                    filename = hashFile + '.' + filename[1]
                    idImPath = filename
                    idProof.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                else:
                    idImPath = None
                    print('No File Uploaded')
            if qualUploadImage:
                filename = secure_filename(qualUploadImage.filename)
                filename = filename.split('.')
                if filename[1] in ALLOWED_EXTENSIONS:
                    hashFile = hashlib.md5(str(filename[0] + str(random.getrandbits(64))).encode()).hexdigest()
                    filename = hashFile + '.' + filename[1]
                    qualImPath = filename
                    print(filename)
                    qualUploadImage.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                qualImPath = None
                print('No File Uploaded')
            if addressProof:
                filename = secure_filename(addressProof.filename)
                filename = filename.split('.')
                if filename[1] in ALLOWED_EXTENSIONS:
                    hashFile = hashlib.md5(str(filename[0] + str(random.getrandbits(64))).encode()).hexdigest()
                    filename = hashFile + '.' + filename[1]
                    addProofIm = filename
                    print(filename)
                    addressProof.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                addProofIm = None
                print('No File Uploaded')
            if appSigImage:
                filename = secure_filename(appSigImage.filename)
                filename = filename.split('.')
                if filename[1] in ALLOWED_EXTENSIONS:
                    hashFile = hashlib.md5(str(filename[0] + str(random.getrandbits(64))).encode()).hexdigest()
                    filename = hashFile + '.' + filename[1]
                    appSigIm = filename
                    print(filename)
                    appSigImage.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                appSigIm = None
                print('No File Uploaded')
        signDate = datetime.utcnow()
        signDate = datetime.date(signDate)
        print(type(signDate))
        newStudent = students(nin=form.NationalInsurance.data, firstName=form.firstName.data,
                              surname=form.lastName.data, email=form.emailAddress.data, token=None,
                              date_birth=form.dateOfBirth.data,degree_id=form.selectCourse.data.degree_id,
                              phone=form.contactNumber.data, address_1=form.fLineAddress.data,
                              address_2=form.sLineAddress.data, city=form.townCity.data,
                              post_code=form.postcode.data, id_staff=1, year_entry=form.entryLevel.data,
                              qualification_image_link=qualImPath, address_proof_image_link=addProofIm,
                              signature_image_link=appSigIm, id_image_link=idImPath, signDate=signDate,
                              confirm=0, dataConfirm=0, filledIn=0, employmentStartDate=form.employmentStartDate.data,
                              jobTitle=form.jobTitle.data)

        db.session.add(newStudent)
        db.session.commit()

        student_id_query = students.query.filter_by(email=form.emailAddress.data).first()
        student_id = student_id_query.id_student

        newEmployer = employer(firstName=form.employerFirstName.data, surname=form.employerSurname.data,
                               employer_email=form.employerEmail.data, token=None,
                               address_1=form.employerFAddress.data, address_2=form.employerSAddress.data,
                               city=form.employerTownCity.data, post_code=form.employerPostcode.data, confirm=0,
                               id_student=student_id)
        db.session.add(newEmployer)
        db.session.commit()
        getEmployer = employer.query.filter_by(employer_email=form.employerEmail.data).first()
        generatedELink = bcrypt.generate_password_hash(str(form.employerEmail.data) +
                                                       str(random.getrandbits(128))).decode('utf-8')
        uploadSigVerify = verify(userID=getEmployer.id_employer, verifyString=generatedELink)
        db.session.add(uploadSigVerify)
        db.session.commit()
        msg = Message('Upload Signature', sender="studentcrmemail@gmail.com",
                      recipients=['studentcrmemail@gmail.com'])
        msg.html = render_template('emailSignature.html', generatedHash=generatedELink)
        mail.send(msg)
        subject = []
        level = []
        grade = []

        subject.append(form.subjectOne.data)
        level.append(form.levelOne.data)
        grade.append(form.gradeOne.data)

        subject.append(form.subjectTwo.data)
        level.append(form.levelTwo.data)
        grade.append(form.gradeTwo.data)

        subject.append(form.subjectThree.data)
        level.append(form.levelThree.data)
        grade.append(form.gradeThree.data)

        subject.append(form.subjectFour.data)
        level.append(form.levelFour.data)
        grade.append(form.gradeFour.data)

        subject.append(form.subjectFive.data)
        level.append(form.levelFive.data)
        grade.append(form.gradeFive.data)

        subject.append(form.subjectSix.data)
        level.append(form.levelSix.data)
        grade.append(form.gradeSix.data)

        subject.append(form.subjectSeven.data)
        level.append(form.levelSeven.data)
        grade.append(form.gradeSeven.data)

        subject.append(form.subjectEight.data)
        level.append(form.levelEight.data)
        grade.append(form.gradeEight.data)

        for x in range(0, 8):
            if subject[x]:
                achievement = achievements(id_student=student_id, subject=subject[x], level=level[x], grade=grade[x])
                db.session.add(achievement)
                db.session.commit()
                print('Added')
        generatedFLink = bcrypt.generate_password_hash(str(form.emailAddress.data) +
                                                  str(random.getrandbits(128))).decode('utf-8')
        newVerify = verify(userID=student_id, verifyString=generatedFLink)
        db.session.add(newVerify)
        db.session.commit()
        msg = Message('Verify Your Account', sender="studentcrmemail@gmail.com",
                      recipients=['studentcrmemail@gmail.com'])
        msg.html = render_template('emailConfirm.html', generatedHash=generatedFLink)
        mail.send(msg)
        print('Done')
        flash('Thanks for registering, please check your email')
        return redirect(url_for('login'))
    elif request.method == 'POST' and form.validate == False:
        if form.NationalInsurance.data is None:
            flash('Empty nin')
        flash('Form not 2222e!')
    else:
        print(form.errors)
        date = datetime.utcnow()

        print(date.strftime("%x"))
        print('Form not validated')

    return render_template('register.html', pageTitle=pageTitle, form=form, date=date, whos=whos)


@app.route('/UploadSigStaff', methods=['GET', 'POST'])
def uploadSigStaff():
    sessions = sessionCheck()
    if 1 in sessions:
        print('Staff Session Found')
    else:
        print('Staff Session Not Found')

    getStaff = staff.query.filter_by(token=session.get('user_token')).first()

    generatedSLink = bcrypt.generate_password_hash(str(getStaff.staff_email) +
                                                   str(random.getrandbits(128))).decode('utf-8')
    uploadSigVerify = verify(userID=getStaff.id_staff, verifyString=generatedSLink)
    db.session.add(uploadSigVerify)
    db.session.commit()
    return redirect("http://127.0.0.1:5000/SignatureUpload?Verify="+generatedSLink+"&Type=staff")


@app.route('/SignatureUpload', methods=['GET', 'POST'])
def uploadSig():
    sessions = sessionCheck()
    if 1 in sessions or 2 in sessions:
        print('Staff Session Found')
    else:
        print('Staff Session Not Found')
    tokenRec = request.args.get('Verify')

    form = UploadSignature()
    if tokenRec:
        print('Got Token')
    else:
        flash('There was an error processing your token. Please contact an administrator.')
        redirect(url_for('home'))

    getVer = verify.query.filter_by(verifyString=tokenRec).first()

    getType = request.args.get('Type')
    print(getType)
    if getType == 'staff':
        checkStaff = staff.query.filter_by(id_staff=getVer.userID).first()
    else:
        checkStaff = False
    if getType == 'employer':
        checkEmployer = employer.query.filter_by(id_employer=getVer.userID).first()
    else:
        checkEmployer = False
    if getVer:
        print('Token Found In DB')
    else:
        flash('There was an error processing your token. Please contact an administrator.')
        redirect(url_for('home'))

    if checkStaff:
        print('Staff Member Uploading Sig')
        if form.validate_on_submit():
            uploadedSignature = request.files.get('uploadFile')
            if uploadedSignature:
                if request.method == 'POST':
                    filename = secure_filename(uploadedSignature.filename)
                    filename = filename.split('.')
                    if filename[1] in ALLOWED_EXTENSIONS:
                        hashFile = hashlib.md5(str(filename[0] + str(random.getrandbits(64))).encode()).hexdigest()
                        filename = hashFile + '.' + filename[1]
                        pathForSig = filename
                        print(filename)
                        uploadedSignature.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    checkStaff.signature_image_link = pathForSig
                    db.session.add(checkStaff)
                    db.session.commit()
                    db.session.delete(getVer)
                    db.session.commit()
                    flash('Thank You For Uploading Your Signature')
                    return redirect(url_for('adminDash'))
                else:
                    print('No File Uploaded')
        return render_template('UploadSignature.html', form=form)
    else:
        print('Not as staff member uploading')

    if checkEmployer:
        print('Employer Uploading Signature')
        if form.validate_on_submit():
            if request.method == 'POST':
                uploadedSignature = request.files.get('uploadFile')
                if uploadedSignature:
                    filename = secure_filename(uploadedSignature.filename)
                    filename = filename.split('.')
                    if filename[1] in ALLOWED_EXTENSIONS:
                        hashFile = hashlib.md5(str(filename[0] + str(random.getrandbits(64))).encode()).hexdigest()
                        filename = hashFile + '.' + filename[1]
                        pathForSig = filename
                        uploadedSignature.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    checkEmployer.signature_image_link = pathForSig
                    db.session.add(checkEmployer)
                    db.session.commit()
                    db.session.delete(getVer)
                    db.session.commit()
                    flash('Thank You For Uploading Your Signature')
                    return redirect(url_for('home'))
                else:
                    print('No File Uploaded')
        return render_template('UploadSignature.html', form=form)
    else:
        print('Not employer uploading')


@app.route('/ConfirmEmail', methods=['GET', 'POST'])
def confEmail():
    tokenRec = request.args.get('Verify')
    userVerify = verify.query.filter_by(verifyString=tokenRec).first()
    studentToVerify = students.query.filter_by(id_student=userVerify.userID).first()
    studentToVerify.confirm = 1
    db.session.add(studentToVerify)
    db.session.commit()
    db.session.delete(userVerify)
    db.session.commit()
    flash('Thank You For Verifying Your Details.')
    return redirect(url_for('login'))


@app.route('/Equality', methods=['GET', 'POST'])
@app.route('/equality', methods=['GET', 'POST'])
def equality():
    pageTitle = "Equality"
    sessions = sessionCheck()
    whos = whoIs()
    if 2 in sessions:
        print('SessionValid')
    else:
        return redirect(url_for('login'))
    whos = whoIs()
    token = str(session.get('user_token'))
    form = EqualityForm()
    studentIDQuery = students.query.filter_by(token=token).first()

    if form.validate_on_submit():
        form.hidden_tag()

        year = datetime.utcnow().year

        newequality = equality_monitoring(degree_id = form.selectCourse.data,
                                        ethnic_group=form.ethnic_group.data,
                                        religion_group=form.religion_group.data,
                                        transgender=form.transgender.data,
                                        sexual_orientation=form.sexual_orientation.data,
                                        care_experience=form.care_experience.data, gender=form.gender.data,
                                        disability=form.disability.data, illness_asperger=form.illness_asperger.data,
                                        illness_blind=form.illness_blind.data, illness_deaf=form.illness_deaf.data,
                                        illness_long=form.illness_long.data, illness_mental=form.illness_mental.data,
                                        illness_learning=form.illness_learning.data,
                                        illness_mobility=form.illness_mobility.data,
                                        illness_not_listed=form.illness_not_listed.data,
                                        illness_not_to_say=form.illness_not_to_say.data,
                                        year=year)
        db.session.add(newequality)
        studentIDQuery.filledIn = 1
        db.session.commit()
        print('Inserted')
        return redirect(url_for('home'))
    elif studentIDQuery.filledIn == True:
        print(form.errors)
        studentIDQuery = students.query.filter_by(token=token).first()
        print("studentid")
        print(studentIDQuery.filledIn)
        flash("You have already completed the Equality Form")
        return redirect(url_for('home'))
    else:
        print('form not validated')
        return render_template('equality.html', pageTitle=pageTitle, form=form, whos=whos)


@app.route('/progressStudent', methods=['GET', 'POST'])
@app.route('/ProgressStudent', methods=['GET', 'POST'])
def progresssstudent():
    pageTitle = "Progress"
    form = StudentProgressForm()
    sessions = sessionCheck()
    whos = whoIs()

    if 2 in sessions:
        print('SessionValid')
    else:
        return redirect(url_for('login'))

    studentQuery = students.query.filter_by(token=session['user_token']).first()
    year = datetime.utcnow().year
    print(year)
    progress_report.query.filter_by(year=year, id_staff_writer = None, id_employer_writer=None).first()
    print (progress_report)
    progress = db.engine.execute(
        "SELECT * FROM progress_report WHERE year = %s AND id_staff_writer IS NULL AND id_employer_writer IS NULL AND id_student = %s ;" %(year, studentQuery.id_student))
    ids = []  #If ids lenght is bigger than 0 means that student has filled up the form
    for row in progress:
        ids.append(row[3])

    if form.validate_on_submit():
        form.hidden_tag()

        year = datetime.utcnow().year

        degreeQuery = degree.query.filter_by(degree_id=studentQuery.degree_id).first()

        newProgressReport = progress_report(id_student=studentQuery.id_student, course_name=degreeQuery.degree_id,
                                            question_1=form.question_1.data, question_2= form.question_2.data,
                                            question_3=form.question_3.data, year=year)
        db.session.add(newProgressReport)
        db.session.commit()

        flash('Thank you for submitting your Progress Report')
        return redirect(url_for('home'))#We need confimation Message
    elif len(ids) > 0:
        flash("You have already completed the Progress Student Form")
        return redirect(url_for('home'))
    else:
        print(form.errors)
        date = datetime.utcnow()
        return render_template('progressstudent.html',pageTitle=pageTitle, form=form, date=date, whos=whos)


@app.route('/evaluationStudent', methods=['GET', 'POST'])
@app.route('/EvaluationStudent', methods=['GET', 'POST'])
def evaluationstudent():
    pageTitle = "Evaluation"
    form = StudentEvaluationForm()
    sessions = sessionCheck()
    whos = whoIs()
    if 2 in sessions:
        print('SessionValid')
    else:
        return redirect(url_for('login'))

    studentQuery = students.query.filter_by(token=session['user_token']).first()
    year = datetime.utcnow().year
    print (progress_report)
    progress = db.engine.execute(
        "SELECT * FROM apprenticeship_evaluation WHERE year = %s AND id_student = %s ;" % (year, studentQuery.id_student))
    ids = []  # If ids lenght is bigger than 0 means that student has filled up the form
    for row in progress:
        ids.append(row[3])

    if form.validate_on_submit():
        form.hidden_tag()

        year = datetime.utcnow().year

        newEvaluationReport = apprenticeship_evaluation(id_student=studentQuery.id_student, overall_exp=form.overall_exp.data,
                            year=year, q_1=form.q_1.data,c_1=form.c_1.data, q_2=form.q_2.data, c_2=form.c_2.data, q_3=form.q_3.data,
                            c_3=form.c_3.data, q_4=form.q_3.data, c_4=form.c_4.data, q_5=form.q_5.data, c_5=form.c_5.data,
                            q_6=form.q_6.data, c_6=form.c_6.data, q_7=form.q_7.data, c_7=form.c_7.data, q_8=form.q_8.data,
                            c_8=form.c_8.data, q_9=form.q_9.data, c_9=form.c_9.data, q_10=form.q_10.data, c_10=form.c_10.data)
        print(newEvaluationReport)
        db.session.add(newEvaluationReport)
        db.session.commit()

        flash('Thank you for submitting your evaluation')
        return redirect(url_for('home'))#We need confimation Message
    elif len(ids) > 0:
        flash("You have already completed the Evaluation Student Report")
        return redirect(url_for('home'))
    else:
        print(form.errors)
        print('form not validated')
        studentToken = session['user_token']
        studentInfo = students.query.filter_by(token=studentToken).first()
        degreeInfo = degree.query.filter_by(degree_id=studentInfo.degree_id).first()
        print(degreeInfo.degree_name)
        return render_template('evaluation.html', pageTitle=pageTitle, form=form, studentInfo=studentInfo,
                               degreeInfo=degreeInfo, whos=whos)


@app.route('/progressEmployer', methods=['GET', 'POST'])
@app.route('/ProgressEmployer', methods=['GET', 'POST'])
def progressemployer():
    pageTitle = "Progress"
    form = EmployerProgressForm()
    sessions = sessionCheck()
    whos = whoIs()
    if 3 in sessions:
        print('SessionValid')
    else:
        return redirect(url_for('login'))
    employerQuery = employer.query.filter_by(token=session['user_token']).first()
    studentQuery = students.query.filter_by(id_student=employerQuery.id_student).first()
    date = datetime.utcnow()
    year = datetime.utcnow().year
    progress = db.engine.execute(
        "SELECT * FROM progress_report WHERE year = %s AND id_employer_writer = %s ;" % (year, employerQuery.id_employer))
    ids = []  # If ids lenght is bigger than 0 means that student has filled up the form
    for row in progress:
        ids.append(row[3])

    if form.validate_on_submit():
        form.hidden_tag()

        year = datetime.utcnow().year
        getEmployer = employer.query.filter_by(token=session.get('user_token')).first()
        degreeQuery = degree.query.filter_by(degree_id=studentQuery.degree_id).first()

        print("degree name")
        print(degreeQuery.degree_id)
        # FIX THIS DATABASE INSERT
        newProgressReport = progress_report(id_employer_writer=getEmployer.id_employer,
                                            id_student=getEmployer.id_student, course_name=degreeQuery.degree_name,
                                            question_1=form.question_1.data, question_2=form.question_2.data, year=year)
        db.session.add(newProgressReport)
        db.session.commit()


        flash('Thank you for submitting your Progress Report')
        return redirect(url_for('home'))  # We need confimation Message
    elif len(ids) > 0:
        flash("You have already completed the Evaluation Student Report")
        return redirect(url_for('home'))
    else:
        print(form.errors)
        print('form not validated')
        return render_template('progressEmployer.html', pageTitle=pageTitle, form=form, whos=whos, date=date)


@app.route('/createStaff', methods=['GET', 'POST'])
@app.route('/CreateStaff', methods=['GET', 'POST'])
def createStaff():
    form = CreateStaff()
    sessions = sessionCheck()
    whos = whoIs()
    if 1 in sessions:
        print('SessionValid')
    else:
        return redirect(url_for('login'))

    if form.validate_on_submit():
        form.hidden_tag()

        checkEmail = validate_email(form.staffEmail.data)

        if checkEmail == False:
            flash('Email Already Exists In Our Database.')
            return redirect(url_for('createStaff'))

        newStaff = staff(staff_email=form.staffEmail.data, firstName=form.staffFirstName.data,
                         surname=form.staffSurname.data, confirm=0)

        db.session.add(newStaff)
        db.session.commit()
        print('New Staff Created')
        return redirect(url_for('login'))
    else:
        print(form.errors)
        print('Form Not Validated')
        return render_template('createStaff.html', form=form, whos=whos)


@app.route('/progressStaff', methods=['GET', 'POST'])
@app.route('/ProgressStaff', methods=['GET', 'POST'])
def progressstaff():
    pageTitle = "Progress"
    form = StaffProgressForm()
    sessions = sessionCheck()
    whos = whoIs()
    if 1 in sessions:
        print('SessionValid')
    else:
        return redirect(url_for('login'))

    if form.validate_on_submit():
        form.hidden_tag()

        staffQuery = staff.query.filter_by(token=session['user_token']).first()
        idStu = request.form.get('idStudent') # Get id of user in dropdownButton

        stu = students.query.filter_by(id_student=idStu).first() #Get studentInfo for following query

        year = datetime.utcnow().year
        degreeQuery = degree.query.filter_by(degree_id=stu.degree_id).first()
        newProgressReport = progress_report(id_staff_writer=staffQuery.id_staff,
                                            id_student=stu.id_student,
                                            course_name=degreeQuery.degree_id,
                                            question_1=form.question_1.data, question_2=form.question_2.data, year=year)
        db.session.add(newProgressReport)
        db.session.commit()
        flash('Thank you for submitting your Progress Report')
        print('Inserted')
        return redirect(url_for('home'))
    else:
        date = datetime.utcnow()
        year = datetime.utcnow().year
        progress = db.engine.execute("SELECT * FROM progress_report WHERE year = %s AND id_staff_writer IS NOT NULL;" %year)
        ids = []
        for row in progress:
            ids.append(row[3])
        sql = 'SELECT * FROM students WHERE id_student NOT IN (' + ','.join((str(n) for n in ids)) + ') ORDER BY surname'
        #sql = 'SELECT * FROM students WHERE id_student NOT IN (SELECT id_student from progress_report ' \
        #      'WHERE id_staff_writer != NULL AND year=%s);' %year
        allStudents = db.engine.execute(sql)
        stu = [dict(id=row[0], name=row[2], surname=row[3], email=row[1]) for row in allStudents.fetchall()]
        print(form.errors)


        return render_template('progressStaff.html', pageTitle=pageTitle, form=form, date=date, stu=stu, whos=whos)


@app.route('/CreateSession', methods=['GET', 'POST'])
@app.route('/createSession', methods=['GET', 'POST'])
def create_session():
    recievedToken = request.args.get('token')
    whos = whoIs()
    print('Token retrieved ' + str(recievedToken))
    studenttokencheck = students.query.filter_by(token=str(recievedToken)).first()
    if studenttokencheck:
        session['user_token'] = str(recievedToken)
        session.permanent = True
        app.permanent_session_lifetime = timedelta(hours=2)
    else:
        print('Non-Student Logging in')
    stafftokencheck = staff.query.filter_by(token=str(recievedToken)).first()
    if stafftokencheck:
        session['user_token'] = str(recievedToken)
        session.permanent = True
        app.permanent_session_lifetime = timedelta(hours=2)
    else:
        print('Non-staff logging in.')
    employertokencheck = employer.query.filter_by(token=str(recievedToken)).first()
    if employertokencheck:
        session['user_token'] = str(recievedToken)
        session.permanent = True
        app.permanent_session_lifetime = timedelta(hours=2)
    else:
        print('Non-employer logging in.')
    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
@app.route('/Login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    sessions = sessionCheck()
    whos = whoIs()
    generatedLink = 0
    print(sessions)
    if 1 in sessions or 2 in sessions or 3 in sessions:
        print('MetThis')
        print('SessionValid')
        return redirect(url_for('home'))
    else:
        print('NOT LOGGED IN')

    if form.validate_on_submit():
        studentLogin = students.query.filter_by(email=form.email.data, confirm=1).first()
        if studentLogin:
            print('Student Login')
            genToken = studentLogin.generate_auth_token()
            studentLogin.token = genToken
            db.session.commit()
            generatedLink = '/CreateSession?token=' + str(genToken)
            msg = Message("Login Token", sender='studentcrmemail@gmail.com',
                          recipients=['studentcrmemail@gmail.com'])
            msg.html = render_template('emailTemplate.html', generatedLink=generatedLink)
            mail.send(msg)
            flash('Login Successful')
            print(generatedLink)
        else:
            print('Email does not exist in students.')

        staffLogin = staff.query.filter_by(staff_email=form.email.data).first()
        if staffLogin:
            print('Staff Login')
            genToken = staffLogin.generate_auth_token()
            staffLogin.token = genToken
            db.session.commit()
            generatedLink = 'CreateSession?token=' + str(genToken)
            print(generatedLink)
            msg = Message("Login Token", sender='studentcrmemail@gmail.com',
                          recipients=['studentcrmemail@gmail.com'])
            msg.html = render_template('emailTemplate.html', generatedLink=generatedLink)
            mail.send(msg)
            flash('Login Successful')
        else:
            print('Email does not exist in staff.')

        employerLogin = employer.query.filter_by(employer_email=form.email.data).first()
        if employerLogin:
            print('Employer Login')
            genToken = employerLogin.generate_auth_token()
            employer.token = genToken
            db.session.commit()
            generatedLink = 'CreateSession?token=' + str(genToken)
            msg = Message("Login Token", sender='studentcrmemail@gmail.com',
                          recipients=['studentcrmemail@gmail.com'])
            msg.html = render_template('emailTemplate.html', generatedLink=generatedLink)
            mail.send(msg)
            flash('Login Successful')
            print(generatedLink)
        else:
            print('Email does not exist in employers.')

        if generatedLink == 0:
            flash(Markup('User does not exist or you have not verified your email. '
                         'You can register <a href="/register" class="alert-link">here</a>.'))
            print("Generated link")
            print(generatedLink)

    else:
        print('Form not validated.')
        generatedLink = 0
    return render_template('login.html', form=form, generatedLink=generatedLink, whos=whos)


@app.route('/ViewProgressForm')
@app.route('/viewProgressForm')
def viewProg():
    sessions = sessionCheck()
    whos = whoIs()
    if 1 in sessions:
        print('SessionValid')
    else:
        return redirect(url_for('login'))

    currentDate = datetime.now()

    studentIDForQuery = request.args.get('ID')

    if studentIDForQuery == None:
        return redirect(url_for('adminDash'))

    studentInfo = students.query.filter_by(id_student=studentIDForQuery).first()

    if studentInfo:
        print('Student Found')
    else:
        print('Student Not Found')

    employerInfo = employer.query.filter_by(id_student=studentIDForQuery).first()
    if employerInfo:
        print('Employer Found')
    else:
        print('Employer Not Found')

    staffInfo = staff.query.filter_by(id_staff=studentInfo.id_staff).first()
    if staffInfo:
        print('Staff Found')
    else:
        print('Staff Not Found')

    progressReportFromStudent = progress_report.query.filter_by(id_student=studentIDForQuery, id_staff_writer=None,
                                                                id_employer_writer=None).first()
    if progressReportFromStudent:
        print('Progress Report Found')
    else:
        print('Progress Report Not Found')

    progressReportFromEmployer = progress_report.query.filter_by(id_student=studentIDForQuery,
                                                                 id_employer_writer=employerInfo.id_employer,
                                                                 id_staff_writer=None).first()
    if progressReportFromEmployer:
        print('Progress Report For Employer Found')
    else:
        print('Progress Report For Employer NOT FOUND')

    progressReportFromStaff = progress_report.query.filter_by(id_student=studentIDForQuery,
                                                              id_staff_writer=studentInfo.id_staff,
                                                              id_employer_writer=None).first()
    if progressReportFromStaff:
        print('Progress Report For Staff Found')
    else:
        print('Progress Report For Staff NOT FOUND')

    return render_template('progress_completed.html', studentInfo=studentInfo, employerInfo=employerInfo,
                           staffInfo=staffInfo, progressReport=progressReportFromStudent,
                           progressReportFromStaff=progressReportFromStaff,
                           progressReportFromEmployer=progressReportFromEmployer, currentDate=currentDate, whos=whos)


@app.route('/ViewEvaluation')
@app.route('/viewEvaluation')
def viewEval():
    sessions = sessionCheck()
    whos = whoIs()
    if 1 in sessions:
        print('SessionValid')
    else:
        return redirect(url_for('login'))


    studentIDForQuery = request.args.get('ID')

    if studentIDForQuery == None:
        return redirect(url_for('adminDash'))

    studentInfo = students.query.filter_by(id_student=studentIDForQuery).first()

    if studentInfo:
        print('Student Info Found')
    else:
        print('Student Info Not Found')

    evalInfo = apprenticeship_evaluation.query.filter_by(id_student=studentIDForQuery).first()

    if evalInfo:
        print('Evaluation Found')
    else:
        print('Evaluation Not Found')
        return redirect(url_for('adminDash'))

    return render_template('evaluation_completed.html', studentInfo=studentInfo, evalInfo=evalInfo, whos=whos)


@app.route('/ViewRegistration')
@app.route('/viewRegistration')
def viewReg():
    sessions = sessionCheck()
    whos = whoIs()
    if 1 in sessions:
        print('SessionValid')
    else:
        return redirect(url_for('login'))


    studentIDForQuery = request.args.get('ID')

    if studentIDForQuery == None:
        return redirect(url_for('adminDash'))

    studentInfo = students.query.filter_by(id_student=studentIDForQuery).first()

    if studentInfo:
        print('Student Found')
    else:
        print('User not found')
        return redirect(url_for('adminDash'))

    staffInfo = staff.query.filter_by(id_staff=studentInfo.id_staff).first()

    if staffInfo:
        print('Staff Info Found')
    else:
        print('Staff Not Found')

    employerInfo = employer.query.filter_by(id_student=studentIDForQuery).first()

    if employerInfo:
        print('Employer Found')
    else:
        print('Employer Not Found')

    getAchievements = achievements.query.filter_by(id_student=studentIDForQuery).all()

    if getAchievements:
        print('Achievements Found')
    else:
        print('Achievements Not Found')

    date = datetime.utcnow()
    return render_template('registration_completed.html', studentInfo=studentInfo, employerInfo=employerInfo,
                           getAchievements=getAchievements, staffInfo=staffInfo, whos=whos,date=date)


@app.route("/Logout")
@app.route("/logout")
def logout():
    if session.get('user_token'):
        session.pop('user_token')
        return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))
