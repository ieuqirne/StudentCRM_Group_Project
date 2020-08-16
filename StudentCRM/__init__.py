import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail, Message
from flask_mysqldb import MySQL

app = Flask(__name__)

UPLOAD_FOLDER = 'C:/Users/enrik/PycharmProjects/SOC09109-2018-9-TR2-001---Group-Project_/StudentCRM/static/Uploads/'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'bmp', 'gif'])

# MySQL configurations
#db = yaml.load(open('db.yaml'))
app.config['SECRET_KEY'] = 'e703f6240aeec11402d4cd300036635ea9da8673e7e52d1019c681691205797b'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///studentscrm.sqlite'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'studentcrmemail@gmail.com'
app.config['MAIL_PASSWORD'] = 'M3z4a6leo!'

#app.config['MYSQL_HOST'] = db['mysql_host']
#app.config['MYSQL_USER'] = db['mysql_user']
#app.config['MYSQL_PASSWORD'] = db['mysql_password']
#app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
LoginManager = LoginManager(app)
mail = Mail(app)
mail.init_app(app)

from StudentCRM import routes
