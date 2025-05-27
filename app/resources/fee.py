from flask_restful import Resource, marshal_with, fields, reqparse, abort
from app.models.fee import FeeModel
from app.extension import db
from datetime import datetime
from dateutil import parser as date_parser

# Request Parser
fee_args = reqparse.RequestParser()
fee_args.add_argument('student_id', type=int, required=True, help="Student ID cannot be empty.")
fee_args.add_argument('amount', type=float, required=True, help="Amount cannot be empty.")
fee_args.add_argument('payment_date', type=str)
fee_args.add_argument('status', type=str, default='pending', help="Status defaults to 'pending'.")
fee_args.add_argument('semester', type=str, help="Semester cannot be empty.")
fee_args.add_argument('fee_type', type=str, required=True, help="Fee type cannot be empty.")

# Response Fields
fee_fields = {
    'id': fields.Integer,
    'student_id': fields.Integer,
    'amount': fields.Float,
    'payment_date': fields.String,
    'status': fields.String,
    'semester': fields.String,
    'fee_type': fields.String
}

class Fees(Resource):
    @marshal_with(fee_fields)
    def get(self):
        """Get all fees
        ---
        tags:
            - Fees
        summary: Retrieve all fees
        description: This endpoint retrieves all fees from the system.
        responses:
            200:
                description: List of all fees retrieved successfully
                schema:
                    type: array
                    items:
                        type: object
                        properties:
                            id:
                                type: integer
                                description: The unique identifier of the fee
                            student_id:
                                type: integer
                                description: The ID of the student
                            amount:
                                type: number
                                format: float
                                description: The amount of the fee
                            fee_type:
                                type: string
                                description: The type of fee
                            semester:
                                type: string
                                description: The semester for the fee
                            payment_date:
                                type: string
                                format: date-time
                                description: The payment date of the fee
                            status:
                                type: string
                                description: The status of the fee payment
            404:
                description: No fees found
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: Fees not found!
        """
        fees = FeeModel.query.all()
        if not fees:
            abort(404, message="Fees not found")
        return fees
       

    @marshal_with(fee_fields)
    def post(self):
        """Create a new fee
        ---
        tags:
            - Fees
        summary: Create a new fee
        description: This endpoint creates a new fee in the system.
        parameters:
            - in: body
              name: fee
              description: Fee data
              required: true
              schema:
                  type: object
                  required:
                      - student_id
                      - amount
                      - fee_type
                  properties:
                      student_id:
                          type: integer
                          description: The ID of the student
                      amount:
                          type: number
                          format: float
                          description: The amount of the fee
                      fee_type:
                          type: string
                          description: The type of fee
                      semester:
                          type: string
                          description: The semester for the fee
                      payment_date:
                          type: string
                          format: date-time
                          description: The payment date of the fee
                      status:
                          type: string
                          description: The status of the fee payment
        responses:
            201:
                description: Fee created successfully
                schema:
                    type: object
                    properties:
                        id:
                            type: integer
                            description: The unique identifier of the created fee
                        student_id:
                            type: integer
                            description: The ID of the student
                        amount:
                            type: number
                            format: float
                            description: The amount of the fee
                        fee_type:
                            type: string
                            description: The type of fee
                        semester:
                            type: string
                            description: The semester for the fee
                        payment_date:
                            type: string
                            format: date-time
                            description: The payment date of the fee
                        status:
                            type: string
                            description: The status of the fee payment
            400:
                description: Bad request - validation error
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: Error message
        """
        args = fee_args.parse_args()
     
      
        # Parse payment_date manually
        payment_date = date_parser.parse(args['payment_date']).date() if args['payment_date'] else None
        try:
            fee = FeeModel(
                student_id=args.student_id,
                amount=args.amount,
                payment_date=payment_date,
                status=args.status,
                semester=args.semester,
                fee_type=args.fee_type
            )
            db.session.add(fee)
            db.session.commit()
            return fee, 201
        except Exception as e:
            db.session.rollback()
            abort(400, message=f"Error: Could not create fee. {str(e)}")

class Fee(Resource):
    @marshal_with(fee_fields)
    def get(self, id):
        """Get a specific fee by ID
        ---
        tags:
            - Fees
        summary: Retrieve a fee by ID
        description: This endpoint retrieves a specific fee by its ID.
        parameters:
            - in: path
              name: id
              type: integer
              required: true
              description: The unique identifier of the fee
        responses:
            200:
                description: Fee retrieved successfully
                schema:
                    type: object
                    properties:
                        id:
                            type: integer
                            description: The unique identifier of the fee
                        student_id:
                            type: integer
                            description: The ID of the student
                        amount:
                            type: number
                            format: float
                            description: The amount of the fee
                        fee_type:
                            type: string
                            description: The type of fee
                        semester:
                            type: string
                            description: The semester for the fee
                        payment_date:
                            type: string
                            format: date-time
                            description: The payment date of the fee
                        status:
                            type: string
                            description: The status of the fee payment
            404:
                description: Fee not found
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: Fee not found!
        """
        fee = FeeModel.query.filter_by(id=id).first()
        if not fee:
            abort(404, message='Fee not found')
        return fee
    
    @marshal_with(fee_fields)
    def put(self, id):
        """Update a fee by ID
        ---
        tags:
            - Fees
        summary: Update a fee
        description: This endpoint updates an existing fee's information.
        parameters:
            - in: path
              name: id
              type: integer
              required: true
              description: The unique identifier of the fee
            - in: body
              name: fee
              description: Updated fee data
              required: true
              schema:
                  type: object
                  required:
                      - student_id
                      - amount
                      - fee_type
                  properties:
                      student_id:
                          type: integer
                          description: The ID of the student
                      amount:
                          type: number
                          format: float
                          description: The amount of the fee
                      fee_type:
                          type: string
                          description: The type of fee
                      semester:
                          type: string
                          description: The semester for the fee
                      payment_date:
                          type: string
                          format: date-time
                          description: The payment date of the fee
                      status:
                          type: string
                          description: The status of the fee payment
        responses:
            200:
                description: Fee updated successfully
                schema:
                    type: object
                    properties:
                        id:
                            type: integer
                            description: The unique identifier of the fee
                        student_id:
                            type: integer
                            description: The ID of the student
                        amount:
                            type: number
                            format: float
                            description: The amount of the fee
                        fee_type:
                            type: string
                            description: The type of fee
                        semester:
                            type: string
                            description: The semester for the fee
                        payment_date:
                            type: string
                            format: date-time
                            description: The payment date of the fee
                        status:
                            type: string
                            description: The status of the fee payment
            404:
                description: Fee not found
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: Fee not found!
            400:
                description: Bad request - validation error
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: Error message
        """
        args = fee_args.parse_args()
        fee = FeeModel.query.filter_by(id=id).first()
        if not fee:
            abort(404, message='Fee not found')
        try:
            fee.student_id = args['student_id']
            fee.amount = args['amount']
            fee.payment_date = args['payment_date']
            fee.status = args['status']
            fee.semester = args['semester']
            fee.fee_type = args['fee_type']
            db.session.commit()
            return fee, 200
        except Exception as e:
            db.session.rollback()
            abort(400, message=f"Error .could not update a fee {str(e)}")
        
    @marshal_with(fee_fields)
    def delete(self, id):
        """Delete a fee by ID
        ---
        tags:
            - Fees
        summary: Delete a fee
        description: This endpoint deletes a fee from the system.
        parameters:
            - in: path
              name: id
              type: integer
              required: true
              description: The unique identifier of the fee
        responses:
            204:
                description: Fee deleted successfully
            404:
                description: Fee not found
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: Fee not found!
            400:
                description: Bad request - error deleting fee
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: Error message
        """
        fee = FeeModel.query.filter_by(id=id).first()
        if not fee:
            abort(404, message='Fee not found')
        try:
            db.session.delete(fee)
            db.session.commit()
            return '', 204
        except Exception as e:
            db.session.rollback()
            abort(400, message=f"Error: Could not delete the fee. {str(e)}")