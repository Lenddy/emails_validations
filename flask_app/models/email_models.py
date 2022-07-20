from flask_app.config.connect_tomysql import connectToMySQL
from flask_app import db,app
from flask  import flash
from flask_bcrypt import Bcrypt
import re
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
bcript = Bcrypt(app)


class Email:
    def __init__(self,data):
        self.id = data ["id"]
        self.email = data["email"]
        self.password = data["password"]

    @classmethod
    def get_all(cls):
        query= "select * from emails;"
        result= connectToMySQL(db).query_db(query)
        return result

    @classmethod
    def add_email_password(cls,data):
        query = "insert into emails (email,password) values(%(email)s,%(password)s);"
        result = connectToMySQL(db).query_db(query,data)
        print(result)
        return result


    @classmethod
    def get_by_email(cls,data):
        query = "select * from emails where email =%(email)s;"
        result = connectToMySQL(db).query_db(query,data)
        return result

    @staticmethod
    def validate_email(user):
        is_valid = True
        if len(user["email"]) == 0:
            flash("no email entered","email_error")
            is_valid = False
        elif not email_regex.match(user["email"]):
            flash("invalid email address format","email_error")
            is_valid = False
        elif Email.get_by_email({"email":user["email"] }) :
            flash("email already in use","email_error")
            is_valid = False
        if len(user["password"]) == 0:
            flash("password must be provided","password")
            is_valid = False
        elif len(user["password"]) < 8:
            flash("password must be at least 8 characters long","password")
            is_valid = False
        return is_valid
