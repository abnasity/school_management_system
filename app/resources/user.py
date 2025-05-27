from flask_restful import Resource,marshal_with,fields,reqparse,abort
from app.extension import db
from app.models.users import UserModel
 # request Parser   
user_args = reqparse.RequestParser()
user_args.add_argument('username',type=str, required=True,help='username cannot be blank')
user_args.add_argument('email',type=str, required=True,help='username cannot be blank')
user_args.add_argument('password',type=str, required=True,help='username cannot be blank')
#output field
user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
    'password':fields.String
}
#resource for all users

class Users(Resource):
    @marshal_with(user_fields)
    #get all users
    def get(self):
        """Get all users
        ---
        tags:
          - Users
        summary: Retrieve all users
        description: This endpoint retrieves all users from the database.
        responses:
          200:
            description: A list of users
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    description: The unique identifier of the user
                  username:
                    type: string
                    description: The username of the user
                  email:
                    type: string
                    description: The email of the user
                  created_at:
                    type: string
                    format: date-time
                    description: The creation date and time of the user
          404:
            description: No users found
            schema:
              type: object
              properties:
                message:
                  type: string
                  description: Users not found!
        """
         #query all users'
        
        
        
        users = UserModel.query.all()
        if not users:
            abort(404,message='Users not found')
        return users
    #create a user
    @marshal_with(user_fields)
    def post(self):
        """Create a new user
        ---
        tags:
            - Users
        summary: Create a new user
        description: This endpoint creates a new user in the system.
        parameters:
            - in: body
              name: user
              description: User data
              required: true
              schema:
                  type: object
                  required:
                      - username
                      - email
                      - password
                  properties:
                      username:
                          type: string
                          description: The username for the user
                      email:
                          type: string
                          description: The email address of the user
                      password:
                          type: string
                          description: The password for the user
        responses:
            201:
                description: User created successfully
                schema:
                    type: object
                    properties:
                        id:
                            type: integer
                            description: The unique identifier of the created user
                        username:
                            type: string
                            description: The username of the user
                        email:
                            type: string
                            description: The email address of the user
                        password:
                            type: string
                            description: The password of the user
            400:
                description: Bad request - validation error
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: Error message
        """
        args = user_args.parse_args()
        try:
            existing_user = UserModel.query.filter_by(username=args['username']).first()
            if existing_user:
                abort(400, message="User with this username already exists")
            new_user = UserModel(username=args['username'], email=args['email'],password=args['password'])
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(400, message=f"There was an error creating the user: {e}")

        users = UserModel.query.all()
        return users, 201
    
class User(Resource):
    @marshal_with(user_fields)
    def get(self,id):
        """Get a specific user by ID
        ---
        tags:
            - Users
        summary: Retrieve a user by ID
        description: This endpoint retrieves a specific user by their ID.
        parameters:
            - in: path
              name: id
              type: integer
              required: true
              description: The unique identifier of the user
        responses:
            200:
                description: User retrieved successfully
                schema:
                    type: object
                    properties:
                        id:
                            type: integer
                            description: The unique identifier of the user
                        username:
                            type: string
                            description: The username of the user
                        email:
                            type: string
                            description: The email address of the user
                        password:
                            type: string
                            description: The password of the user
            404:
                description: User not found
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: User not found!
        """
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort (404,message='User not found')
        return user
    
    @marshal_with(user_fields)
    def patch(self,id):
        """Update a user by ID
        ---
        tags:
            - Users
        summary: Update a user
        description: This endpoint updates an existing user's information.
        parameters:
            - in: path
              name: id
              type: integer
              required: true
              description: The unique identifier of the user
            - in: body
              name: user
              description: Updated user data
              required: true
              schema:
                  type: object
                  required:
                      - username
                      - email
                      - password
                  properties:
                      username:
                          type: string
                          description: The username for the user
                      email:
                          type: string
                          description: The email address of the user
                      password:
                          type: string
                          description: The password for the user
        responses:
            200:
                description: User updated successfully
                schema:
                    type: object
                    properties:
                        id:
                            type: integer
                            description: The unique identifier of the user
                        username:
                            type: string
                            description: The username of the user
                        email:
                            type: string
                            description: The email address of the user
                        password:
                            type: string
                            description: The password of the user
            404:
                description: User not found
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: User not found!
        """
        args = user_args.parse_args()
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404,message='no user with that id')
        user.username = args['username']
        user.email = args['email']
        user.password = args['password']
        db.session.commit()
        return user  

    @marshal_with(user_fields) 
    def delete(self,id):
        """Delete a user by ID
        ---
        tags:
            - Users
        summary: Delete a user
        description: This endpoint deletes a user from the system.
        parameters:
            - in: path
              name: id
              type: integer
              required: true
              description: The unique identifier of the user
        responses:
            200:
                description: User deleted successfully and remaining users returned
                schema:
                    type: array
                    items:
                        type: object
                        properties:
                            id:
                                type: integer
                                description: The unique identifier of the user
                            username:
                                type: string
                                description: The username of the user
                            email:
                                type: string
                                description: The email address of the user
                            password:
                                type: string
                                description: The password of the user
            404:
                description: User not found
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            description: User not found!
        """
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404,message="cannot delete a non existing user")
        db.session.delete(user)
        db.session.commit()
        return f'user deleted successfully'
   





