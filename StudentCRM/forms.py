from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, \
    FileField, TextField, validators
from wtforms.widgets import TextArea
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from wtforms.fields.html5 import DateField
from StudentCRM.models import students, employer, staff, degree, progress_report
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms_components import DateTimeField, DateRange
from datetime import datetime, date, timedelta
from StudentCRM import db
from flask import session
from wtforms.validators import NumberRange

def degree_choices():
    return degree.query

def checkEqualityIsFilledUp(id):

    return filled


class RegistrationForm(FlaskForm):
    NationalInsurance = StringField('National Insurance Number', validators=[DataRequired(),
    Regexp('^\s*[a-zA-Z]{2}(?:\s*\d\s*){6}[a-zA-Z]?\s*$', 0,
           'Incorrect NIN Format: AA000000A')])
    firstName = StringField('First Name', validators=[DataRequired(), Length(min=2, max=30)])
    lastName = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=30)])
    dateOfBirth = DateField('Date of Birth', validators=[DateRange(max=date.today() - timedelta(days=17*365))])
    emailAddress = StringField('Email Address', validators=[DataRequired(), Email()])
    contactNumber = StringField('Contact Telephone Number', validators=[DataRequired(), Length(min=5,max=15)])
    fLineAddress = StringField('First Line of Address', validators=[DataRequired()])
    sLineAddress = StringField('Second Line of Address', validators=[validators.Optional()])
    townCity = StringField('Town or City', validators=[DataRequired(), Length(min=2, max=20)])
    postcode = StringField('Postcode', validators=[DataRequired(), Length(max=8)])
    selectCourse = QuerySelectField(query_factory=degree_choices, allow_blank=False, get_label='degree_name')
    startDate = SelectField('Course Start Date', choices=[("1", "09/09/2019")], validators=[DataRequired()])
    entryLevel = SelectField('Apprenticeship Entry Level',  choices=[('1', '1'), ('2', '2'),
                                                            ('3', '3'), ('4', '4')], validators=[DataRequired()])
    courseLength = SelectField('Course Length', choices=[('1', '1 Year'), ('2', '2 Years'),
                                                         ('3', '3 Years'), ('4', '4 Years'),
                                                         ('5', '5 Years')], validators=[DataRequired()])
    employerFirstName = StringField('Employer First Name', validators=[DataRequired(), Length(min=2, max=30)])
    employerSurname = StringField('Employer Surname', validators=[DataRequired(), Length(min=2, max=30)])
    employerEmail = StringField('Employer Email', validators=[DataRequired(), Email()])
    employmentStartDate = DateField('Employment Start Date', validators=[DataRequired()])
    employerFAddress = StringField('Employer First Line of Address', validators=[DataRequired()])
    employerSAddress = StringField('Employer Second Line of Address', validators=[validators.Optional()])
    employerTownCity = StringField('Employer Town or City', validators=[DataRequired(), Length(min=2, max=20)])
    employerPostcode = StringField('Employer Postcode', validators=[DataRequired(), Length(max=8)])
    jobTitle = StringField('Job Title', validators=[DataRequired()])

    subjectOne = StringField('Subject One')
    levelOne = SelectField('Level One', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
                                                         ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'),
                                                     ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12')],
                                            validators=[DataRequired()])
    gradeOne = SelectField('Grade One', choices=[('A', 'A'), ('B', 'B'), ('C', 'C'),('D', 'D'), ('E', 'E')],
                           validators=[DataRequired()])
    subjectTwo = StringField('Subject Two')
    levelTwo = SelectField('Level Two', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
                                                         ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'),
                                                     ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12')],
                                            validators=[DataRequired()])
    gradeTwo = SelectField('Grade Two', choices=[('A', 'A'),('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E')],
                           validators=[DataRequired()])
    subjectThree = StringField('Subject Three')
    levelThree = SelectField('Level Three', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
                                                         ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'),
                                                     ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12')],
                                            validators=[DataRequired()])
    gradeThree = SelectField('Grade Three', choices=[('A', 'A'), ('B', 'B'), ('C', 'C'),
                                                         ('D', 'D'), ('E', 'E')], validators=[DataRequired()])
    subjectFour = StringField('Subject Four')
    levelFour = SelectField('Level Four', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
                                                         ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'),
                                                     ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12')],
                                            validators=[DataRequired()])
    gradeFour = SelectField('Grade Four', choices=[('A', 'A'), ('B', 'B'), ('C', 'C'),
                                                         ('D', 'D'), ('E', 'E')], validators=[DataRequired()])
    subjectFive = StringField('Subject Five')
    levelFive = SelectField('Level Five', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
                                                         ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'),
                                                     ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12')],
                                            validators=[DataRequired()])
    gradeFive = SelectField('Grade Five', choices=[('A', 'A'), ('B', 'B'), ('C', 'C'),
                                                         ('D', 'D'), ('E', 'E')], validators=[DataRequired()])
    subjectSix = StringField('Subject Six')
    levelSix = SelectField('Level Six', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
                                                         ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'),
                                                     ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12')],
                                            validators=[DataRequired()])
    gradeSix = SelectField('Grade Six', choices=[('A', 'A'), ('B', 'B'), ('C', 'C'),
                                                         ('D', 'D'), ('E', 'E')], validators=[DataRequired()])
    subjectSeven = StringField('Subject Seven')
    levelSeven = SelectField('Level Seven', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
                                                         ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'),
                                                     ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12')],
                                            validators=[DataRequired()])
    gradeSeven = SelectField('Grade Seven', choices=[('A', 'A'), ('B', 'B'), ('C', 'C'),
                                                         ('D', 'D'), ('E', 'E')], validators=[DataRequired()])
    subjectEight = StringField('Subject Eight')
    levelEight = SelectField('Level Eight', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
                                                         ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'),
                                                     ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12')],
                                            validators=[DataRequired()])
    gradeEight = SelectField('Grade Eight', choices=[('A', 'A'), ('B', 'B'), ('C', 'C'),
                                                         ('D', 'D'), ('E', 'E')], validators=[DataRequired()])
    termsAndConditionsCheck = BooleanField('Agree Checkbox', validators=[DataRequired()])
    # CHECK NEEDS TO BE DONE ON FILE TO ENSURE THERE IS AN IMAGE!!
    apprenticeSignature = FileField('Image File', validators=[DataRequired()])
    # CHECK NEEDS TO BE DONE ON FILE TO ENSURE THERE IS AN IMAGE!!
    qualificationProofImage = FileField('Proof of Qualification Image', validators=[DataRequired()])
    # CHECK NEEDS TO BE DONE ON FILE TO ENSURE THERE IS AN IMAGE!!
    addressProofImage = FileField('Proof of Address Image', validators=[DataRequired()])
    idProofImage = FileField('Proof of ID Image', validators=[DataRequired()])

    submit = SubmitField('Register')

    def validate_email(self, emailAddress):
        emailCheckStudent = students.query.filter_by(email=emailAddress).first()
        emailCheckEmployer = employer.query.filter_by(employer_email=emailAddress).first()
        emailCheckStaff = staff.query.filter_by(staff_email=emailAddress).first()
        if emailCheckStudent or emailCheckStaff or emailCheckEmployer:
            print('Email Already Exists in our database.')
            raise ValidationError('Email Address Exists In Our Database')


class EditProfileForm(FlaskForm):
    NationalInsurance = StringField('National Insurance Number', validators=[DataRequired(),
    Regexp('^\s*[a-zA-Z]{2}(?:\s*\d\s*){6}[a-zA-Z]?\s*$', 0,
           'Incorrect NIN Format: AA000000A')])
    firstName = StringField('First Name', validators=[DataRequired(), Length(min=2, max=30)])
    lastName = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=30)])
    dateOfBirth = DateField('Date of Birth', validators=[DateRange(max=date.today() - timedelta(days=17*365))])
    emailAddress = StringField('Email Address', validators=[DataRequired(), Email()])
    contactNumber = StringField('Contact Telephone Number', validators=[DataRequired(), Length(min=5,max=20)])
    fLineAddress = StringField('First Line of Address', validators=[DataRequired()])
    sLineAddress = StringField('Second Line of Address')
    townCity = StringField('Town or City', validators=[DataRequired(), Length(min=2,max=20)])
    postcode = StringField('Postcode', validators=[DataRequired(), Length(max=8)])
    selectCourse = QuerySelectField(query_factory=degree_choices, allow_blank=False, get_label='degree_name')
    startDate = SelectField('Course Start Date', choices=[("1", "09/09/2019")], validators=[DataRequired()])
    entryLevel = SelectField('Apprenticeship Entry Level',  choices=[('1', '1'), ('2', '2'),
                                                            ('3', '3'), ('4', '4')], validators=[DataRequired()])
    courseLength = SelectField('Course Length', choices=[('1', '1 Year'), ('2', '2 Years'),
                                                         ('3', '3 Years'), ('4', '4 Years'),
                                                         ('5', '5 Years')], validators=[DataRequired()])
    employerFirstName = StringField('Employer First Name', validators=[DataRequired(), Length(min=2, max=30)])
    employerSurname = StringField('Employer Surname', validators=[DataRequired(), Length(min=2, max=30)])
    employerEmail = StringField('Employer Email', validators=[DataRequired(), Email()])
    employmentStartDate = DateField('Employment Start Date', validators=[DataRequired()])
    employerFAddress = StringField('Employer First Line of Address', validators=[DataRequired()])
    employerSAddress = StringField('Employer Second Line of Address', validators=[DataRequired()])
    employerTownCity = StringField('Employer Town or City', validators=[DataRequired(), Length(min=2, max=20)])
    employerPostcode = StringField('Employer Postcode', validators=[DataRequired(), Length(max=8)])
    jobTitle = StringField('Job Title', validators=[DataRequired()])

    subjectOne = StringField('Subject One')
    levelOne = IntegerField('Level One', validators=[validators.Optional(), NumberRange(min=1, max=12,
                                                                 message='Level must be between 1 and 12')])
    gradeOne = StringField('Grade One', validators=[validators.Optional(),
            Regexp('^[A-D]$', 0, '[A,B,C,D,E]')])
    subjectTwo = StringField('Subject Two')
    levelTwo = IntegerField('Level Two', validators=[validators.Optional(), NumberRange(min=1, max=12,
                                                                 message='Level must be between 1 and 12')])
    gradeTwo = StringField('Grade Two', validators=[validators.Optional(),
            Regexp('^[A-D]$', 0, '[A,B,C,D,E]')])
    subjectThree = StringField('Subject Three')
    levelThree = IntegerField('Level Three', validators=[validators.Optional(), NumberRange(min=1, max=12,
                                                                 message='Level must be between 1 and 12')])
    gradeThree = StringField('Grade Three', validators=[validators.Optional(),
            Regexp('^[A-D]$', 0, '[A,B,C,D,E]')])
    subjectFour = StringField('Subject Four')
    levelFour = IntegerField('Level Four', validators=[validators.Optional(), NumberRange(min=1, max=12,
                                                                 message='Level must be between 1 and 12')])
    gradeFour = StringField('Grade Four', validators=[validators.Optional(),
            Regexp('^[A-D]$', 0, '[A,B,C,D,E]')])
    subjectFive = StringField('Subject Five')
    levelFive = IntegerField('Level Five', validators=[validators.Optional(), NumberRange(min=1, max=12,
                                                                 message='Level must be between 1 and 12')])
    gradeFive = StringField('Grade Five', validators=[validators.Optional(),
            Regexp('^[A-D]$', 0, '[A,B,C,D,E]')])
    subjectSix = StringField('Subject Six')
    levelSix = IntegerField('Level Six', validators=[validators.Optional(), NumberRange(min=1, max=12,
                                                                 message='Level must be between 1 and 12')])
    gradeSix = StringField('Grade Six',  validators=[validators.Optional(),
            Regexp('^[A-D]$', 0, '[A,B,C,D,E]')])
    subjectSeven = StringField('Subject Seven')
    levelSeven = IntegerField('Level Seven', validators=[validators.Optional(), NumberRange(min=1, max=12,
                                                                 message='Level must be between 1 and 12')])
    gradeSeven = StringField('Grade Seven', validators=[validators.Optional(),
            Regexp('^[A-D]$', 0, '[A,B,C,D,E]')])
    subjectEight = StringField('Subject Eight')
    levelEight = IntegerField('Level Eight', validators=[validators.Optional(), NumberRange(min=1, max=12,
                                                                 message='Level must be between 1 and 12')])
    gradeEight = StringField('Grade Eight', validators=[validators.Optional(),
            Regexp('^[A-D]$', 0, '[A,B,C,D,E]')])

    # CHECK NEEDS TO BE DONE ON FILE TO ENSURE THERE IS AN IMAGE!!
    apprenticeSignature = FileField('Image File')
    # CHECK NEEDS TO BE DONE ON FILE TO ENSURE THERE IS AN IMAGE!!
    qualificationProofImage = FileField('Proof of Qualification Image')
    # CHECK NEEDS TO BE DONE ON FILE TO ENSURE THERE IS AN IMAGE!!
    addressProofImage = FileField('Proof of Address Image')
    submit = SubmitField('Update')

    def validate_email(self, emailAddress):
        emailCheckStudent = students.query.filter_by(email=emailAddress).first()
        emailCheckEmployer = employer.query.filter_by(employer_email=emailAddress).first()
        emailCheckStaff = staff.query.filter_by(staff_email=emailAddress).first()
        if emailCheckStudent or emailCheckStaff or emailCheckEmployer:
            print('Email Already Exists in our database.')
            raise ValidationError('Email Address Exists In Our Database')


class TestFileUpload(FlaskForm):
    file1 = FileField('Image File')
    file2 = FileField('Image File')
    file3 = FileField('Image File')
    submit = SubmitField('Submit')


class EqualityForm(FlaskForm):
    selectCourse = SelectField('Please select your course:', choices=[('1', 'Construction and the Built Environment'),
                                                         ('2', 'Civil Engineering(SCQF 8)'),
                                                         ('3','Civil Engineering(SCQF 10)'),
                                                         ('4', 'Engineering: Design and Manufacture'),
                                                         ('5', 'Engineering: Instrumentation, Measurement and Control'),
                                                         ('6', 'Business Management: Financial Services'),
                                                         ('7', 'IT: Management for Business'),
                                                         ('8','IT: Software Development'),
                                                         ('9', 'CyberSecurity (SCQF 10)'),
                                                         ('10','CyberSecurity (SCQF 11)'),
                                                         ('11', 'Business Management')])
    entryLevel = SelectField('Apprenticeship Entry Level: ', choices=[('1', 'Year 1'), ('2', 'Year 2'),
                                                     ('3', 'Year 3'), ('4', 'Year 4'),
                                                     ('5', 'Year 5')], validators=[DataRequired()])
    courseLength = SelectField('Length of Programme:', choices=[('1', '1 Year'), ('2', '2 Years'),
                                                     ('3', '3 Years'), ('4', '4 Years'),
                                                     ('5', '5 Years')], validators=[DataRequired()])
    ethnic_group = SelectField('1. Ethnic Group:', choices=[('1', 'Scottish'),
                                                         ('2', 'Other British'),
                                                         ('3', 'Irish'),
                                                         ('4', 'Other White Background'),
                                                         ('5', 'Mixed ethnic background'),
                                                         ('6', 'Pakistani'),
                                                         ('7', 'Indian'),
                                                         ('8', 'Bangladeshi'),
                                                         ('9', 'Chinese'),
                                                         ('10', 'Other Asian Background'),
                                                         ('11', 'African'),
                                                         ('12', 'Caribbean'),
                                                         ('13', 'Other black background'),
                                                         ('14', 'Other ethnic background'),
                                                         ('15', 'Prefer not to say'),
                                                         ('16', 'Not known')])
    ethnic_groupText = ('Please select the option below that most closely describes you')
    religion_group = SelectField('2. Religion or Belief:', choices=[('1', 'None'),
                                                             ('2', 'Church of Scotland'),
                                                             ('3', 'Roman Catholic'),
                                                             ('4', 'Other Christian'),
                                                             ('5', 'Muslim'),
                                                             ('6', 'Buddhist'),
                                                             ('7', 'Sikh'),
                                                             ('8', 'Jewish'),
                                                             ('9', 'Hindu'),
                                                             ('10', 'Pagan'),
                                                             ('11', 'Other'),
                                                             ('12', 'Prefer not to say')])
    religion_groupText = 'Please indicate your religion or belief from the following options: '
    transgender = SelectField('3. Transgender', choices=[('1', 'Yes'),
                                                         ('2', 'No'),
                                                         ('3', 'Prefer not to say')])
    transgenderText='Have you ever indentified as transgender?'
    sexual_orientation = SelectField('4. Sexual Orientation', choices=[('1', 'Hetrosexual/Straight'),
                                                             ('2', 'Gay/Lesbian'),
                                                             ('3', 'Bisexual'),
                                                             ('4', 'Other'),
                                                             ('5', 'Prefer not to say')])
    sexual_orientationText = 'Do you consider yourself to be?'
    care_experience = SelectField('5. Care Experience', choices=[('1', 'Yes'),
                                                             ('2', 'No'),
                                                             ('3', 'Prefer not to say')])
    care_experienceText1 = 'Have you ever been in care*?'
    care_experienceText2 = ('*In care means you are or were formally looked after by a local authority, in the family '
                            'home (with support from social services or a social worker) or elsewhere,'
                            ' for example, in foster care,'
                            ' residential/secure care, or kinship care (with family friends or relatives).')
    gender = SelectField('1. Gender', choices=[('1', 'Male'),
                                                             ('2', 'Female')])
    disability = SelectField('2. Disability', choices=[('1', 'Yes'),
                                                             ('2', 'No'),
                                                             ('3', 'Prefer not to say')])
    disabilityText = ('The information you provide in this section will help us provide an inclusive environment for disabled\
                            people, by identifying and removing barriers in our practices.')
    disabilityText2 = '1. Do you have an impairment, health condition or learning difficulty?*'
    disabilityText3 = '*Lasting or expected to last 12 months or more'

    illness = ('2. If you have an impairment, health condition or learning difficulty, please\
                        select all those on the list that apply.')
    illness_aspergerText = ('You have a social/communication impairment such as a speech and language impairment '
                            'or Asperger’s syndrome/other autistic spectrum disorder, or\
                                    cognitive impairment')
    illness_asperger = BooleanField('Asperger')
    illness_blindText = ('You are blind or have a visual '
                         'impairment uncorrected by glasses')
    illness_blind = BooleanField('Blind')
    illness_deafText = ('You are deaf or have a '
                        'hearing impairment')
    illness_deaf = BooleanField('Deaf')
    illness_longText = ('You have a long standing illness or health '
                        'condition such as cancer, HIV, diabetes, chronic heart disease, or epilepsy')
    illness_long = BooleanField('Long')
    illness_mentalText = ('You have a mental health difficulty,'
                          ' such as depression, schizophrenia or anxiety disorder')
    illness_mental = BooleanField('Mental')
    illness_learningText = ('You have a specific learning difficulty '
                            'such as dyslexia, dyspraxia or AD(H)D')
    illness_learning = BooleanField('Learning')
    illness_mobilityText = ('You have a physical impairment or mobility issues, such as '
                            'difficulty using your arms or using a wheelchair or crutches')
    illness_mobility = BooleanField('Mobility')
    illness_not_listedText = ('You have a disability, impairment or medical condition that is not listed above.')
    illness_not_listed = BooleanField('Mobility')
    illness_not_to_sayText = ('Prefer not to say')
    illness_not_to_say = BooleanField('Mobility')
    readCheck = BooleanField('I have read and accept the SDS Graduate Apprenticeship Privacy', validators=[DataRequired()])
    endText = ('The completed and signed section B is retained at all times by the Learning Provider for inspection,\
                    and Section A is securely disposed of as soon as copies of the Participant’s responses in Sections A\
                    and B have been sent to SDS. Please note that an individual must not be registered as a participant on\
                    the programme until the form has been completed fully in accordance with these instructions.')
    submit = SubmitField('Submit')


class StudentProgressForm(FlaskForm):
    question_1 = TextField('Please provide detail on your progress both on campus and in the workplace. '
                           'For example, detail any additional tasks or '
                           'responsibilities which you now carry out.', widget=TextArea(),
                           validators=[DataRequired(), Length(min=15, max=200)])
    question_2 = TextField('Please detail how the process of reflection on work practice and reviewing '
                           'and learning from experience is integrated into '
                           'your experience on campus and in the work place.', widget=TextArea(),
                           validators=[DataRequired(), Length(min=15, max=200)])
    question_3 = TextField('Please provide any additional comments on the GA programme which you would like to provide.'
                           , widget=TextArea(), validators=[DataRequired(), Length(min=15, max=200)])
    submit = SubmitField('Submit')


class StudentEvaluationForm(FlaskForm):
    overall_exp = SelectField('On a scale 1 to 5, how satisfied or dissatisfied are you by your '
                              'overall experience of your Graduate Apprendiceship\
                            so far? Please choose the appropriate answer:',
                              choices=[('1', '1. Very dissatisfied'),
                                       ('2', '2. Quite dissatisfied'),
                                       ('3', '3. Neither satisfied or dissatisfied'),
                                       ('4', '4. Quite satisfied'),
                                       ('5', '5. Very Satisfied')])
    q_1 = SelectField('I am supported by my university/college in all areas of my graduate apprenticeship.',
                      choices=[('1', '1. Completely disagree'),
                               ('2', '2. Somewhat disagree'),
                               ('3', '3. Neither agree or disagree'),
                               ('4', '4. Somewhat agree'),
                               ('5', '5. Completely agree')])
    c_1 = StringField('Comments: ', widget=TextArea(), validators=[DataRequired(), Length(min=2, max=200)])
    q_2 = SelectField('I can access all on campues facilities, such as the library, support services, '
                      'student onion etc, at my university/college.', choices=[('1', '1. Completely disagree'),
                                                                               ('2', '2. Somewhat disagree'),
                                                                               ('3', '3. Neither agree or disagree'),
                                                                               ('4', '4. Somewhat agree'),
                                                                               ('5', '5. Completely agree')])
    c_2 = StringField('Comments: ', widget=TextArea(), validators=[DataRequired(), Length(min=2, max=200)])
    q_3 = SelectField('I feel part of the wider learning community on campus. ',
                      choices=[('1', '1. Completely disagree'),
                               ('2', '2. Somewhat disagree'),
                               ('3', '3. Neither agree or disagree'),
                               ('4', '4. Somewhat agree'),
                               ('5', '5. Completely agree')])
    c_3 = StringField('Comments: ', widget=TextArea(), validators=[DataRequired(), Length(min=2, max=200)])
    q_4 = SelectField('My individual learning plan is responsive to the needs of my job role'
                      '(for example, there is minimal assessment during busy times at work.)',
                      choices=[('1', '1. Completely disagree'),
                               ('2', '2. Somewhat disagree'),
                               ('3', '3. Neither agree or disagree'),
                               ('4', '4. Somewhat agree'),
                               ('5', '5. Completely agree')])
    c_4 = StringField('Comments: ', widget=TextArea(), validators=[DataRequired(), Length(min=2, max=200)])
    q_5 = SelectField('I feel supported by my fellow graduate apprentices.',
                      choices=[('1', '1. Completely disagree'),
                               ('2', '2. Somewhat disagree'),
                               ('3', '3. Neither agree or disagree'),
                               ('4', '4. Somewhat agree'),
                               ('5', '5. Completely agree')])
    c_5 = StringField('Comments: ', widget=TextArea(), validators=[DataRequired(), Length(min=2, max=200)])
    q_6 = SelectField('I can use my learning from my graduate apprenticeship and apply it directly to my job role.',
                      choices=[('1', '1. Completely disagree'),
                               ('2', '2. Somewhat disagree'),
                               ('3', '3. Neither agree or disagree'),
                               ('4', '4. Somewhat agree'),
                               ('5', '5. Completely agree')])
    c_6 = StringField('Comments: ', widget=TextArea(), validators=[DataRequired(), Length(min=2, max=200)])
    q_7 = SelectField('I am supported by my employer in all areas of my graduate.',
                                                choices=[('1', '1. Completely disagree'),
                                                         ('2', '2. Somewhat disagree'),
                                                         ('3', '3. Neither agree or disagree'),
                                                         ('4', '4. Somewhat agree'),
                                                         ('5', '5. Completely agree')])
    c_7 = StringField('Comments: ', widget=TextArea(), validators=[DataRequired(), Length(min=2, max=200)])
    q_8 = SelectField('I have access to relevant resources in my workplace to support my graduate apprenticeship.',
                                                choices=[('1', '1. Completely disagree'),
                                                         ('2', '2. Somewhat disagree'),
                                                         ('3', '3. Neither agree or disagree'),
                                                         ('4', '4. Somewhat agree'),
                                                         ('5', '5. Completely agree')])
    c_8 = StringField('Comments: ', widget=TextArea(), validators=[DataRequired(), Length(min=2, max=200)])
    q_9 = SelectField('My workplace mentor provides useful support in my graduate apprenticeships.',
                                                choices=[('1', '1. Completely disagree'),
                                                         ('2', '2. Somewhat disagree'),
                                                         ('3', '3. Neither agree or disagree'),
                                                         ('4', '4. Somewhat agree'),
                                                         ('5', '5. Completely agree')])
    c_9 = StringField('Comments: ', widget=TextArea(), validators=[DataRequired(), Length(min=2, max=200)])
    q_10 = SelectField('My graduate apprenticeship is helping to improve my future employability.',
                                                choices=[('1', '1. Completely disagree'),
                                                         ('2', '2. Somewhat disagree'),
                                                         ('3', '3. Neither agree or disagree'),
                                                         ('4', '4. Somewhat agree'),
                                                         ('5', '5. Completely agree')])
    c_10 = StringField('Comments: ', widget=TextArea(), validators=[DataRequired(), Length(min=2, max=200)])

    submit = SubmitField('Submit')

class EmployerProgressForm(FlaskForm):
    allCourses = degree.query.all()
    question_1 = TextField('Please provide details of any support in place for apprentices to assist their progression and achievement.', widget=TextArea(),
                validators=[DataRequired(), Length(min=15, max=200)])
    question_2 = TextField('Please provide detail on how you, as the employer, contributed to shaping your apprentice’s learning plan.', widget=TextArea(),
                validators=[DataRequired(), Length(min=15, max=200)])

    submit = SubmitField('Submit')


def allStudents():
    return students.query


class StaffProgressForm(FlaskForm):
    question_1 = TextField('Please provide details of any support in place for apprentices to assist their progression and achievement.', widget=TextArea(),
                validators=[DataRequired(), Length(min=15, max=200)])
    question_2 = TextField('Please provide detail on how you, as the employer, contributed to shaping your apprentice’s learning plan.', widget=TextArea(),
                validators=[DataRequired(), Length(min=15, max=200)])
    submit = SubmitField('Submit')


#class AdminDashForm(FlaskForm):
    #Students = students.query.all()


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    remember = BooleanField('Remember Me?')
    submit = SubmitField('Login')


class UploadSignature(FlaskForm):
    uploadFile = FileField('Upload Signature', validators=[DataRequired()])
    submit = SubmitField('Upload')


class CreateStaff(FlaskForm):
    staffFirstName = StringField('staffFirstName', validators=[DataRequired()])
    staffSurname = StringField('staffSurname', validators=[DataRequired()])
    staffEmail = StringField('staffEmail', validators=[DataRequired(), Email()])
    submit = SubmitField('Register New Staff Member')
