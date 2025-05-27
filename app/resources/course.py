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
        """Create a new course
        ---
        tags:
            - Courses
        summary: Create a new course
        description: This endpoint creates a new course in the system.
        parameters:
            - in: body
              name: course
              description: Course data
              required: true
              schema:
                  type: object
                  required:
                      - code
                      - name
                      - credits
                  properties:
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
        responses:
            201:
                description: Course created successfully
                schema:
                    type: object
                    properties:
                        id:
                            type: integer
                            description: The unique identifier of the created course
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
            400:
                description: Bad request - validation error
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: Error message
        """
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
            return course, 201
        except Exception as e:
            db.session.rollback()
            abort(400, message=f"Error creating course: {str(e)}")
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
        """Get a specific course by ID
        ---
        tags:
            - Courses
        summary: Retrieve a course by ID
        description: This endpoint retrieves a specific course by its ID.
        parameters:
            - in: path
              name: id
              type: integer
              required: true
              description: The unique identifier of the course
        responses:
            200:
                description: Course retrieved successfully
                schema:
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
                description: Course not found
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: Course not found!
        """
        course = CourseModel.query.filter_by(id=id).first()
        if not course:
            abort(404, message="Course not found")
        return course
    
      
        
        

    @marshal_with(course_fields)
    def put(self, id):
        """Update a course by ID
        ---
        tags:
            - Courses
        summary: Update a course
        description: This endpoint updates an existing course's information.
        parameters:
            - in: path
              name: id
              type: integer
              required: true
              description: The unique identifier of the course
            - in: body
              name: course
              description: Updated course data
              required: true
              schema:
                  type: object
                  required:
                      - code
                      - name
                      - credits
                  properties:
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
        responses:
            200:
                description: Course updated successfully
                schema:
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
                description: Course not found
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: Course not found!
            400:
                description: Bad request - validation error
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: Error message
        """
        args = course_args.parse_args()
        course = CourseModel.query.filter_by(id=id).first()
        if not course:
            abort(404, message="Course not found")
        try:
            course.code = args['code']
            course.name = args['name']
            course.credits = args['credits']
            course.teacher_id = args['teacher_id']
            db.session.commit()
            return course
        except Exception as e:
            db.session.rollback()
            abort(400, message=f"Error updating course: {str(e)}")
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
        """Delete a course by ID
        ---
        tags:
            - Courses
        summary: Delete a course
        description: This endpoint deletes a course from the system.
        parameters:
            - in: path
              name: id
              type: integer
              required: true
              description: The unique identifier of the course
        responses:
            204:
                description: Course deleted successfully
            404:
                description: Course not found
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: Course not found!
            400:
                description: Bad request - error deleting course
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: Error message
        """
        course = CourseModel.query.filter_by(id=id).first()
        if not course:
            abort(404, message="Course not found")
        try:
            db.session.delete(course)
            db.session.commit()
            return '', 204
        except Exception as e:
            db.session.rollback()
            abort(400, message=f"Error deleting course: {str(e)}")
     