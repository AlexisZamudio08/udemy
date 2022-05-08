from dotenv import load_dotenv
import os
import pymysql.cursors

class Item:
    @classmethod
    def __init__(cls, _id: int, _name: str, _price: float) -> None:
        cls.id = _id
        cls.name = _name
        cls.price = _price

    @classmethod
    def to_json(cls) -> dict:
        return {'name': cls.name, 'price': cls.price}

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
    def find_by_name(cls) -> object:
        connection = cls.create_connection()
        with connection.cursor() as cursor:
            sql = "SELECT * FROM items WHERE name=%s"
            cursor.execute(sql, (cls.name,))
            result = cursor.fetchone()
            if result:
                return cls(result['id'], result['name'], result['price'])
            else:
                return None
    
    @classmethod
    def insert(cls) -> object:
        '''
        This method is used to insert a new item in the database.
        if the implementation is successful, it will return the item object,
        otherwise it will return None.
        '''
        connection = cls.create_connection()
        with connection.cursor() as cursor:
            sql = "INSERT INTO items (name, price) VALUES (%s, %s)"
            res = cursor.execute(sql, (cls.name, cls.price))
            connection.commit()
            if res: 
                return cls.find_by_name()
            else:
                return None

    @classmethod
    def update(cls) -> None:
        '''
        This method is used to update an item in the database.
        if the implementation is successful, it will return the item object,
        otherwise it will return None.
        '''
        connection = cls.create_connection()
        with connection.cursor() as cursor:
            sql = "UPDATE items SET price=%s WHERE name=%s"
            res = cursor.execute(sql, (cls.price, cls.name))
            connection.commit()
            if res:
                return cls.find_by_name()
            else:
                return None

    @classmethod
    def delete(cls) -> None:
        '''
        This method is used to delete an item in the database.
        if the implementation is successful, it will return the item object,
        otherwise it will return None.
        '''
        connection = cls.create_connection()
        with connection.cursor() as cursor:
            sql = "DELETE FROM items WHERE name=%s"
            res = cursor.execute(sql, (cls.name,))
            connection.commit()
            if res:
                return cls.to_json()
            else:
                return None


    
    @classmethod
    def get_items(cls) -> list:
        '''
        This method is used to get all items from the database.
        '''
        connection = cls.create_connection()
        with connection.cursor() as cursor:
            sql = "SELECT * FROM items"
            cursor.execute(sql)
            result = cursor.fetchall()
            if result:
                return result
            else:
                return None
