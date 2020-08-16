cd venv/scripts
call activate
cd../..
pip install -r requirements.txt
cd StudentCRM
set FLASK_APP=../run.py
set FLASK_ENV=development

flask run
