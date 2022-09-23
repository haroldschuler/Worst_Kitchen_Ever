from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash, session

class Ingredient:
    def __init__(self,data):
        self.id = data['id']
        self.ingredient_name = data['ingredient_name']
        self.spoonacular_id = data['spoonacular_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def search_ingredients_by_text(cls,data):
        query = "SELECT * FROM ingredients WHERE ingredient_name LIKE %(ingredient_name)s;"
        results = connectToMySQL('my_kitchen_schema').query_db(query,data)
        ingredients = []
        if len(results) > 0:
            for item in results:
                ingredients.append(cls(item))
        return ingredients