from flask_restful import Resource, abort, marshal_with, fields, reqparse
from app.extension import db
from app.models.enrollment import EnrollmentModel
from datetime import datetime
from dateutil import parser as date_parser 

#Request Parser
enrollment_args = reqparse.RequestParser()
enrollment_args.add_argument('student_id', type=int, help="Student ID cannot be empty")
enrollment_args.add_argument('course_id', type=str, help="Course ID cannot be empty")
enrollment_args.add_argument('enrollment_date', type=date_parser)
enrollment_args.add_argument('status', type=str, default='active') #if the client does not provide a status value it'll be set to active by default