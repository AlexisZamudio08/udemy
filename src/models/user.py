from werkzeug.security import check_password_hash, generate_password_hash 
from dotenv import load_dotenv
import os
import pymysql.cursors

class User:
    @classmethod
    def __init__(cls, _id: int, _username: str, _password: str) -> None:
        cls.id = _id
        cls.username = _username
        cls.password = _password

    @classmethod
    def to_json(cls) -> dict:
        return {
            'id': cls.id,
            'username': cls.username,
            'password': cls.password
        }

    @classmethod
    def create_connection(cls) -> object:
        '''
        This method is used to create a connection to the database.
        '''
        load_dotenv('../.venv')
        connection = pymysql.connect(host=os.getenv('MYSQL_DATABASE_HOST'),
                                 user=os.getenv('MYSQL_DATABASE_USER'),
                                 password=os.getenv('MYSQL_DATABASE_PASSWORD'),
                                 database=os.getenv('MYSQL_DATABASE_DB'),
                                 cursorclass=pymysql.cursors.DictCursor)
        return connection
    
    @classmethod
    def check_password(cls, hashed_password: str, password: str) -> bool:
        '''
        This method is used to check if the password match with the hashed storage.
        '''
        return check_password_hash(hashed_password, password)

    @classmethod
    def crate_hash(cls, password: str) -> str:
        '''
        This method is used to create a hash for the password.
        '''
        hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
        return hash

    @classmethod
    def find_by_id(cls) -> object:
        '''
        This method is used to find a user by id.
        '''
        connection = cls.create_connection()
        with connection:
            with connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT * FROM `users` WHERE `id` = %s"
                cursor.execute(sql, (cls.id,))
                result = cursor.fetchone()
                if result is None:
                    return None
                else:
                    return cls(result['id'], result['username'], result['password'])

    @classmethod
    def find_by_username(cls) -> object:
        connection = cls.create_connection()
        with connection:
            with connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT * FROM `users` WHERE `username` = %s"
                cursor.execute(sql, (cls.username,))
                result = cursor.fetchone()
                if result is None:
                    return None
                else:
                    return cls(result['id'], result['username'], result['password'])
    @classmethod
    def find_all(cls) -> list:
        connection = cls.create_connection()
        with connection:
            with connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT * FROM `users`"
                cursor.execute(sql)
                result = cursor.fetchall()
                if result is None:
                    return None
                else:
                    users = {}
                    for user in result:
                        users[user['id']] =  {'username' : user['username'], 'password': user['password']}
                    return users

    @classmethod
    def insert(cls) -> dict:
        '''
        This method is used to create a user.
        '''
        connection = cls.create_connection()
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO users (id, username, password) VALUES (%s,%s,%s)", (0, cls.username, cls.crate_hash(cls.password)))
            connection.commit()
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE username = %s", (cls.username,))
                result = cursor.fetchone()
                if result is None:
                    return None
                else:
                    return {'id': result['id'], 'username': result['username']}

    @classmethod
    def update(cls) -> dict:
        '''
        This method is used to update a user.
        '''
        connection = cls.create_connection()
        with connection:
           with connection.cursor() as cursor:
               cursor.execute("UPDATE users SET password = %s WHERE username = %s", (cls.crate_hash(cls.password), cls.username))
           connection.commit()
           with connection.cursor() as cursor:
               cursor.execute("SELECT * FROM users WHERE username = %s", (cls.username,))
               result = cursor.fetchone()
               if result is None:
                   return None
               else:
                   return {'id': result['id'], 'username': result['username']}

    @classmethod
    def delete(cls) -> None:
        '''
        This method is used to delete a user.
        '''
        connection = cls.create_connection()
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM users WHERE id = %s", (cls.id,))
            connection.commit()
            return {'message': 'User deleted'}