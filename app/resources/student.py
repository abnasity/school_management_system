from flask_restful import Resource, abort, marshal_with, fields, reqparse
from app.extension import db
from app.models.student import StudentModel
from dateutil.parser import parser as date_parse

# Request Parser
student_args = reqparse.RequestParser()
student_args.add_argument('first_name',type=str, required=True, help="First name cannot be empty")
student_args.add_argument('last_name', type=str, required=True, help="Last name cannot be empty")
student_args.add_argument('student_id', type=str, required=True, help="Student ID cannot be blank")
student_args.add_argument('email', type=str, required=True, help="student email cannot be blank")
student_args.add_argument('date_of_birth', type=date_parse)
student_args.add_argument('enrollment_date', type=date_parse)


# output field
student_fields = {
    'id':fields.Integer,
    'first_name':fields.String,
    'last_name':fields.String,
    'student_id':fields.String,
    'email':fields.String,
    'date_of_birth':fields.DateTime,
    'enrollment_date':fields.DateTime
}

# Resources
class Students(Resource):
    # Get all students
    @marshal_with(student_fields)
    def get(self):
        students = StudentModel.query.all()
        if not students:
            abort(404, message='Students not found')
        return students
    
  # Create a student
    @marshal_with(student_fields)
    def post(self):
        args = student_args.parse_args()
        student = StudentModel(**args)
        db.session.add(student)
        db.session.commit()
        return student, 201
    
# Specific student, edit and delete a student
class Student(Resource):
    @marshal_with(student_fields)
    def get(self, id):
        student = StudentModel.query.filter_by(id=id).first()
        if not student:
            abort(404, message='Student not found')
        return student, 200
    
    
    @marshal_with(student_fields)
    def put(self, id):
        args = student_args.parse_args()
        student = StudentModel.query.filter_by(id=id).first()
        if not student:
            abort(404, message='Student not found')
        # for key, value in args.items():
        #     setattr(student, key, value)
        student.first_name = args['first_name']
        student.last_name = args['last_name']
        student.student_id = args['student_id']
        student.email = args['email']
        student.date_of_birth = args['date_of_birth']
        student.enrollment_date = args['enrollment_date']
        db.session.commit()
        return student, 200
    
    
# Delete a student
    @marshal_with(student_fields)
    def delete(self, id):
        student = StudentModel.query.filter_by(id=id).first()
        if not student:
            abort(404, message='Student not found')
        db.session.delete(student)
        db.session.commit()
        return '', 204