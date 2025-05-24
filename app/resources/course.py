from flask_restful import Resource, abort, marshal_with, fields, reqparse
from app.extension import db
from app.models.course import CourseModel
from dateutil import parser as date_parser


# REQUEST PARSER
course_args = reqparse.RequestParser()
course_args.add_argument('code', type=int, required=True, help="Course code cannot be empty")
course_args.add_argument('name', type=str, required=True, help="Course name cannot be empty")
course_args.add_argument('credits', type=int, default=0, help="Credits must be an integer")
course_args.add_argument('teacher_id', type=int, required=True, help="Teacher ID is required")


# COURSE FIELDS
course_fields = {
    'id' : fields.Integer,
    'code': fields.String,
    'name': fields.String,
    'credits': fields.Integer,
    'teacher_id': fields.Integer
}