from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash, session, request
from flask_bcrypt import Bcrypt
import re

#update these regex checks as needed
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$')
bcrypt = Bcrypt(app)

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def register_user(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        result = connectToMySQL('my_kitchen_schema').query_db(query, data)
        return result

    @classmethod
    def get_user_from_id(cls,user_id):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL('my_kitchen_schema').query_db(query, user_id)
        return cls(result[0])

    @classmethod
    def does_email_exist(cls, answers):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('my_kitchen_schema').query_db(query, answers)
        if len(result) < 1:
            print('email does NOT exist')
            return False
        else:
            print('email does exist')
            return True

    @staticmethod
    def validate_login(data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('my_kitchen_schema').query_db(query, data)
        if len(result) < 1:
            flash('Invalid email','login_error')
            return False
        elif bcrypt.check_password_hash(result[0]['password'],data['password']) == False:
            flash('Invalid password','login_error')
            return False
        else:
            session['user_id'] = result[0]['id']
            session['user_name'] = result[0]['first_name']
            print(session['user_name'] + " is logged in with session")
            return True

    @staticmethod
    def validate_registration(answers):
        is_valid = True
        if len(answers['first_name']) < 2:
            flash('First name must be at least 2 characters','registration_error')
            is_valid = False
        if len(answers['last_name']) < 2:
            flash('Last name must be at least 2 characters','registration_error')
            is_valid = False
        if not EMAIL_REGEX.match(answers['email']):
            flash('Invalid email address','registration_error')
            is_valid = False
        elif User.does_email_exist(answers) == True:
            flash('Email address already taken','registration_error')
            is_valid = False
        if not PASSWORD_REGEX.match(answers['password']):
            flash('Password must be at least 8 characters and contain 1 upper case, 1 lower case character, and 1 digit','registration_error')
            is_valid = False
        elif answers['password'] != answers['conf_password']:
            flash('Passwords do not match','registration_error')
            is_valid = False
        return is_valid