from app.extension import db
from datetime import datetime, timezone


class FeeModel(db.Model):
    __tablename__='fees'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    fee_type = db.Column(db.String(50), nullable=False) #tuition, accomodation, graduation
    semester = db.Column(db.String(20))
    payment_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    status = db.Column(db.String(20), default='pending')#paid, overdue
    
    def __repr__(self):
        return f"Fee {self.id - {self.fee_type}}"