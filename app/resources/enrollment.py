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

# Response Fields
enrollment_fields = {
    'id' : fields.Integer,
    'student_id' : fields.Integer,
    'course_id' : fields.Integer,
    'enrollment_date' : fields.DateTime,
    'status' : fields.String
}


# Enrollments Resource
class Enrollment(Resource):
    @marshal_with(enrollment_fields)
    def get(self, id):
        # Implement the logic for GET request here
        # For example, return all enrollments
        enrollments = EnrollmentModel.query.filter_by(id=id).first
        if not enrollments:
            abort (404, message="Enrollments not found")
        return enrollments
    
    @marshal_with(enrollment_fields)
    def post(self):
        args = enrollment_args.parse_args()
        try:
            enrollment = EnrollmentModel(
                student_id=args['student_id'],
                course_id=args['course_id'],
                enrollment_date=args['enrollment_date'],
                status=args['status']
            )
            db.session.add(enrollment)
            db.session.commit()
            return enrollment, 201
        except Exception as e:
            db.session.rollback()
            abort(400, message=f"Error: Could not create an enrollment. {str(e)}")
            
    @marshal_with(enrollment_fields)
    def patch(self, id):
        args = enrollment_args.parse_args()
        enrollment = EnrollmentModel.query.filter_by(id=id).first()
        if not enrollment:
            abort(404, message="Enrollment not found")
        try:
            enrollment.student_id = args['student_id']
       
            enrollment.course_id = args['course_id']

            enrollment.enrollment_date = args['enrollment_date']
       
            enrollment.status = args['status']
            db.session.commit()
            return enrollment, 200
        except Exception as e:
             db.session.rollback()
             abort(400, message=f"could not update the enrollment. {str(e)}")