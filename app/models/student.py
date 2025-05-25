from app.extension import db
from datetime import datetime,timezone
from app.models.enrollment import EnrollmentModel
from app.models.fee import FeeModel 

class StudentModel(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80),nullable=False)
    last_name = db.Column(db.String(80),nullable=False)
    student_id = db.Column(db.String(200),nullable=False,unique=True)
    email = db.Column(db.String(120),nullable=False,unique=True)
    date_of_birth = db.Column(db.Date)
    enrollment_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    enrollments = db.relationship('EnrollmentModel', backref='student',lazy=True)
    fees = db.relationship('FeeModel', backref='student_ref',lazy=True)

    def __repr__(self):
        return f"{self.student_id} {self.first_name} {self.last_name}"
    