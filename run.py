import os
from flask_migrate import Migrate
from StudentCRM import app
from StudentCRM import db
from StudentCRM.models import students, achievements, staff, employer, progress_report, degree, \
    apprenticeship_evaluation, equality_monitoring

migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(students=students, achievements=achievements, staff=staff, progress_report=progress_report,
                employer=employer, degree=degree, apprenticeship_evaluation=apprenticeship_evaluation,
                equality_monitoring=equality_monitoring)

if __name__ == '__main__':
    app.run(debug=True)
