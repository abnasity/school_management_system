from flask_restful import Resource, abort, marshal_with, fields, reqparse
from app.extension import db
from app.models.course import CourseModel



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

# Resources
class Courses(Resource):
    # Get all students
    @marshal_with(course_fields)
    def get(self):
        """Get all courses
        ---
        tags:
            - Courses
        summary: Retrieve all courses
        description: This endpoint retrieves all courses from the system.
        responses:
            200:
                description: List of all courses retrieved successfully
                schema:
                    type: array
                    items:
                        type: object
                        properties:
                            id:
                                type: integer
                                description: The unique identifier of the course
                            code:
                                type: string
                                description: The course code
                            name:
                                type: string
                                description: The name of the course
                            credits:
                                type: integer
                                description: The number of credits for the course
                            teacher_id:
                                type: integer
                                description: The ID of the assigned teacher
            404:
                description: No courses found
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: Courses not found!
        """
        
        
        
        
        courses = CourseModel.query.all()
        if not courses:
            abort(404, message="Courses not found")
        return courses


# COURSE RESOURCE

    
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
        
class Course(Resource):
    @marshal_with(course_fields)
    def get(self, id):
        courses = CourseModel.query.filter_by(id=id).first
        if not courses:
            abort(404, message="Course not found")
        return courses
        
        

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
           
    