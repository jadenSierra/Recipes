from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)
import re

DB = "recipes_schema"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instruction = data['instruction']
        self.date = data['date']
        self.quick = data['quick']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data["user_id"]

    @classmethod
    def save(cls,data):
        query = "INSERT INTO recipes (name, description, instruction, date , quick , created_at,updated_at, user_id) VALUES ( %(recipe_name)s,%(recipe_description)s,%(recipe_instructions)s,%(recipe_date)s, %(recipe_quick)s ,NOW(), NOW(), %(user_id)s);"
        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(DB).query_db(query,data)


    @classmethod
    def get_all(cls):
        query= "SELECT * FROM recipes;"
        results = connectToMySQL(DB).query_db(query)
        recipes = []
        for recipe in results:
            recipes.append( cls(recipe) )
        return recipes

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL(DB).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM recipes WHERE id = %(id)s"
        result = connectToMySQL(DB).query_db(query, data)
        print(result)
        return result

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True 
        if len(recipe['recipe_name']) <= 2:
            flash("Name must be at least 2 characters.", "name_error")
            is_valid = False
        if len(recipe['recipe_description']) < 10:
            flash("Description must be at least 10 characters.", "description_error")
            is_valid = False
        if len(recipe['recipe_instructions']) < 10:
            flash("Instructions must be atleast 10 characters long.", "instructions_error")
            is_valid = False
        if len(recipe['recipe_date']) < 1:
            flash("Please enter a date.", "date_error")
            is_valid = False

        return is_valid


    @classmethod
    def update(cls,data):
        query = "UPDATE recipes SET name= %(recipe_name)s, description = %(recipe_description)s, instruction = %(recipe_instructions)s, date=%(recipe_date)s, quick = %(recipe_quick)s, updated_at=NOW() WHERE id = %(recipe_id)s;"
        return connectToMySQL(DB).query_db(query,data)