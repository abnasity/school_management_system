from flask import Flask
from app.extension import db
from flask_restful import Api
from app.resources.user import Users,User
from app.resources.teacher import Teachers
from config import Config
from flask_migrate import Migrate




app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
api = Api(app)
migrate = Migrate(app,db)

 #api endpoints
api.add_resource(Users,'/api/users/')
api.add_resource(User,'/api/users/<int:id>')
api.add_resource(Teachers, '/api/teachers')
         



