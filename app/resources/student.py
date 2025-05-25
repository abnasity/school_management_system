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