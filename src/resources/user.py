from models.user import User
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
       type=str,
       required=True,
       help="This field cannot be left blank!"
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    def get(self, username=None):
        if username:
            user = User(0, username, None)
            res = user.find_by_username()
            if res: 
                return {"user": user.to_json()}, 200
            else:
                return {"message": "User not found"}, 404
        res = User.find_all()
        return res, 200

    @jwt_required()
    def post(self):
        data = UserRegister.parser.parse_args()
        user = User(0, data['username'], data['password'])
        exist = user.find_by_username()
        if exist:
            return {"message": "User already exists"}, 400
        else:
            status = user.insert()
            if status:
                return {"user": status}, 201
            else:
                return {"message": "Something went wrong"}, 500
    #@jwt_required
    def put(self):
        data = UserRegister.parser.parse_args()
        user = User(0, data['username'], data['password'])
        exist = user.find_by_username()
        if exist:
            user = User(0, data['username'], data['password'])
            res = user.update()
            if res: 
                return {"message": "User updated"}, 202
            else: return {"message": "Something went wrong"}, 500
        else:
            res = user.insert()
            if res: return res, 201
            else: return {"message": "Something went wrong"}, 500

    
    @jwt_required()
    def delete(self, username):
        user = User(0, username, '')
        exist = user.find_by_username()
        if exist:
            status = user.delete()
            if status:
                return {"message": "User deleted"}, 200
            else:
                return {"message": "Something went wrong"}, 500
        else:
            return {"message": "User not found"}, 404
        


    