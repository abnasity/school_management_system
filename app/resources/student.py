from flask_restful import Resource, abort, marshal_with, fields, reqparse
from app.extension import db
from app.models.student import StudentModel


# Request Parser