from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)
import re

DB = "recipes_schema"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password ,created_at,updated_at) VALUES ( %(first_name)s,%(last_name)s,%(email)s,%(password)s, NOW(), NOW());"
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL(DB).query_db(query,data)


    @classmethod
    def get_all(cls):
        query= "SELECT * FROM users;"
        results = connectToMySQL(DB).query_db(query)
        users = []
        for user in results:
            users.append( cls(user) )
        return users

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(DB).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL(DB).query_db(query, data)

        if len(result) < 1:
            return False

        return cls(result[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL(DB).query_db(query, data)
        print(result)
        return result

    @staticmethod
    def validate_user(user):
        is_valid = True # we assume this is true

        if len(user['first_name']) <= 2:
            flash("First name must be at least 2 characters.", "first_name_error")
            is_valid = False
        if len(user['last_name']) <= 2:
            flash("Last name must be at least 2 characters.", "last_name_error")
            is_valid = False
        if len(user['email']) < 3:
            flash("Invalid email address!", 'email_error')
            is_valid = False
        elif not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!")
            is_valid = False
        if len(user['password']) <= 7:
            flash("Password must be atleast 8 characters long.", "password_error")
            is_valid = False
        if user['password'] != user['password_confirmation']:
            flash("Passwords dont match.", "password_confirmation_error")
            is_valid = False
        return is_valid


    @staticmethod
    def is_valid(email):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DB).query_db(query,email)
        if len(results) >= 1:
            flash("Email already taken.")
            is_valid=False
        if not EMAIL_REGEX.match(email['email']):
            flash("Invalid Email.")
            is_valid=False
        return is_valid


    # @classmethod
    # def email_exsists(cls, data):
    #     query = "SELECT * FROM users WHERE email = %(email)s"
    #     result = connectToMySQL(DB).query_db(query, data)
    #     print(result)
    #     if result:
    #         return True
    #     if not result:
    #         return False
