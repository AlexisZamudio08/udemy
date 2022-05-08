from models.user import User

def authenticate(username, password):
    user = User(0, username, password)
    user = user.find_by_username()
    if user and User.check_password(user.password, password):
        return user
    return None

def identity(payload):
    user_id = payload['identity']
    user = User(user_id, '', '')
    return user.find_by_id()

    #user = User.find_by_id(user_id)
    #user = next(user, None)
    #return user