from flask_restful import Resource, marshal_with, fields, reqparse, abort
from app.models.student import StudentModel
from app.extension import db
from dateutil import parser as date_parser

# Request parser
student_args = reqparse.RequestParser()
student_args.add_argument('first_name', type=str, required=True, help="First Name of student cannot be empty")
student_args.add_argument('last_name', type=str, required=True, help="Last Name of student cannot be empty")
student_args.add_argument('student_id', type=str, required=True, help="Student ID cannot be empty")
student_args.add_argument('email', type=str, required=True, help="Email of student cannot be empty")
student_args.add_argument('date_of_birth', type=str, required=False)  # We'll parse manually
student_args.add_argument('enrollment_date', type=str, required=False)  # Fix typo here

# Response fields
student_fields = {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'student_id': fields.String,
    'email': fields.String,
    'date_of_birth': fields.String,  # can be DateTime, but keep string if you want isoformat
    'enrollment_date': fields.String,
}

# Student Resource
class Students(Resource):
    @marshal_with(student_fields)
    def get(self):
        students = StudentModel.query.all()
        if not students:
            abort(404, message='Students not found')
        return students

    @marshal_with(student_fields)
    def post(self):
        args = student_args.parse_args()
        try:
            # Parse dates manually
            dob = date_parser.parse(args['date_of_birth']).date() if args['date_of_birth'] else None
            enroll_date = date_parser.parse(args['enrollment_date']) if args['enrollment_date'] else None
            
            student = StudentModel(
                first_name=args['first_name'],
                last_name=args['last_name'],
                student_id=args['student_id'],
                email=args['email'],
                date_of_birth=dob,
                enrollment_date=enroll_date
            )
            db.session.add(student)
            db.session.commit()
            return student, 201
        except Exception as e:
            db.session.rollback()
            abort(400, message=f"Error could not create a student: {str(e)}")

class Student(Resource):
    @marshal_with(student_fields)
    def get(self, id):
        student = StudentModel.query.filter_by(id=id).first()
        if not student:
            abort(404, message='Student not found')
        return student

    @marshal_with(student_fields)
    def put(self, id):
        args = student_args.parse_args()
        student = StudentModel.query.filter_by(id=id).first()
        if not student:
            abort(404, message='Student not found')
        try:
            dob = date_parser.parse(args['date_of_birth']).date() if args['date_of_birth'] else None
            enroll_date = date_parser.parse(args['enrollment_date']) if args['enrollment_date'] else None

            student.first_name = args['first_name']
            student.last_name = args['last_name']
            student.student_id = args['student_id']
            student.email = args['email']
            student.date_of_birth = dob
            student.enrollment_date = enroll_date
            
            db.session.commit()
            return student, 200
        except Exception as e:
            db.session.rollback()
            abort(400, message=f"Error could not update a student: {str(e)}")

    @marshal_with(student_fields)
    def patch(self, id):
        args = student_args.parse_args()
        student = StudentModel.query.filter_by(id=id).first()
        if not student:
            abort(404, message='Student not found')
        try:
            
            student.first_name = args['first_name']
            
            student.last_name = args['last_name']
            
            student.student_id = args['student_id']
            
            student.email = args['email']
            
            student.date_of_birth = date_parser.parse(args['date_of_birth']).date()
            
            student.enrollment_date = date_parser.parse(args['enrollment_date'])
            
            db.session.commit()
            return student, 200
        except Exception as e:
            db.session.rollback()
            abort(400, message=f"Error could not update a student: {str(e)}")

    def delete(self, id):
        student = StudentModel.query.filter_by(id=id).first()
        if not student:
            abort(404, message='Student not found')
        db.session.delete(student)
        db.session.commit()
        return '', 204
