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


# COURSE RESOURCE
class CourseModel(Resource):
    @marshal_with(course_fields)
    def get(self, id):
        courses = CourseModel.query.filter_by(id=id).first
        if not courses:
            abort(404, message="Course not found")
        return courses
    
    @marshal_with(course_fields)
    def post(self):
        args = course_args.parse_args()
        try:
            course = CourseModel(
                code=args['code'],
                name=args['name'],
                credits=args['credits'],
                teacher_id=args['teacher_id']
            )
            db.session.add(course)
            db.session.commit()
            return course,201
        except Exception as e:
            db.session.rollback()
            abort(400, message=f"Error. could not create course {str(e)}")
        
    @marshal_with(course_fields)
    def put(self, id):
        args = course_args.parse_args
        course = CourseModel.query.filter_by(id=id).first()
        if not course:
            abort(404, message="Could not find course")
        try:
            
            course.code = args['code']
            course.name = args['name']
            course.credits = args['credits']
            course.teacher_id = args['teacher_id']
            
            
            db.session.commit()
            return course,200
        except Exception as e:
            db.session.rollback()
            abort(400, message=f"Error. could not update a course {str(e)}")
        
        
    @marshal_with(course_fields)
    def patch(self, id):
        args = course_args.parse_args()
        course = CourseModel.query.filter_by(id=id).first()
        if not course:
            abort(404, message="Could not find course")
        try:
            
            course.code = args['code']
            
            course.name = args['name']
            
            course.credits = args['credits']
            
            course.teacher_id = args['teacher_id']
            
            db.session.commit()
            return course,200
        except Exception as e:
            db.session.rollback()
            abort(400, message=f"Error. could not update a course {str(e)}")
            
    @marshal_with(course_fields)
    def delete(self, id):
     course = CourseModel.query.filter_by(id=id).first()
     if not course:
          abort(400, message="Course not found")
     try:
            db.session.delete(course)
            db.session.commit()
            return'', 204
     except Exception as e:
            db.session.rollback()
            abort(404, message=f"Error. could not delete the course {str(e)}")
           
    