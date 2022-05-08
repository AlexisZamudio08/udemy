#---------------- IMPORTS -------------------# 
from http.client import HTTPResponse
from dotenv import load_dotenv
from flask import Flask, jsonify
import os

#To handle connections to the database.
from flaskext.mysql import MySQL
import flaskext.mysql as mysql

#crsf token protection
#from flask_wtf.csrf import CSRFProtect

#Api resources 
from flask_restful import Resource, Api, reqparse

#auth resources
from flask_jwt import JWT, jwt_required
from pkg_resources import require
from security import authenticate, identity

#------------- CONFIGURATION ----------------# 
from config import config

#---------- MODELS AND CONTROLLERS ----------#
from models.item import Item
from models.user import User

from resources.item import ItemRegister
from resources.user import UserRegister

#---------- SECRET KEY LOAD -----------------#
def load_env_var():
    load_dotenv('../.venv')
    secretKey = os.getenv('SECRET_KEY')
    return secretKey

#------------- APP INITIALIZATION -----------#
app = Flask(__name__)
api = Api(app)

#----------------- DATABASE ------------------#
#    db = MySQL()
#    db.init_app(app)

#------ AUTHENTICATION AND AUTHORIZATION -----#
#csrf = CSRFProtect()
app.secret_key = load_env_var()
jwt = JWT(app, authenticate, identity) # /auth 

#----------------- ROUTES -------------------#
# class User(Resource):
#     #@jwt_required()
#     def get(self, name, args=None):
#         if args: return {'/test/{}'.format(name): args}, 200
#         else: return {'/name/{}'.format(name): 'GET'}, 200

#     #@jwt_required()
#     def post(self, name):
#         #next(filter(lambda x: x['name'] == name, items), None)
#         return self.get(name, 'POST')

#     #@jwt_required()
#     def put(self, name):
#         return self.get(name, 'PUT')
    
#     #@jwt_required()
#     def delete(self, name):
#         return self.get(name, 'DELETE')

# class OtherRoute(Resource):
#     def get(self):
#         return {'route': '/others'}, 200

api.add_resource(UserRegister, '/user')
api.add_resource(UserRegister, '/user/<username>', endpoint='user')
api.add_resource(ItemRegister, '/item')
api.add_resource(ItemRegister, '/item/<name>', endpoint='item')

#api.add_resource(User, '/user/<string:name>')
#api.add_resource(OtherRoute, '/others')


def status_404(error):
    return jsonify({'message': 'Not found'}), 404

if __name__ == '__main__':
    #add configuration to the web app
    app.config.from_object(config['default'])
    #manage page 404
    app.register_error_handler(404, status_404)
    #start the web app
    app.run()