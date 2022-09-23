from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash, session



class Recipe:
    def __init__(self,data):
        self.id = data['id']
        self.spoonacular_id = data['spoonacular_id']
        self.recipe_name = data['recipe_name']
        self.image_link = data['image_link']
        self.missed_ingredients = data['missed_ingredients']
        self.instructions = data['instructions']
        self.cook_time = data['cook_time']
        self.full_ingredient_list = data['full_ingredient_list']
        self.credit = data['credit']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_recipe(cls,data):
        query = "INSERT INTO recipes (spoonacular_id, recipe_name, image_link, missed_ingredients) VALUES (%(spoonacular_id)s, %(recipe_name)s, %(image_link)s, %(missed_ingredients)s);"
        results = connectToMySQL('my_kitchen_schema').query_db(query,data)
        return results
    
    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL('my_kitchen_schema').query_db(query)
        recipes = []
        for item in results:
            recipes.append(cls(item))
        for item in recipes:
            item.missed_ingredients = item.missed_ingredients.split(",")
        # print(recipes[1])
        return recipes
    
    @classmethod
    def get_one_recipe_by_id(cls,data):
        query = "SELECT * FROM recipes WHERE id=%(id)s;"
        results = connectToMySQL('my_kitchen_schema').query_db(query,data)
        return cls(results[0])

    @classmethod
    def update_recipe(cls, data):
        query = "UPDATE recipes SET instructions = %(instructions)s, cook_time = %(cook_time)s, full_ingredient_list = %(full_ingredient_list)s, credit = %(credit)s, updated_at = NOW() WHERE id = %(id)s;"
        results = connectToMySQL('my_kitchen_schema').query_db(query,data)
        return results

    @classmethod
    def delete_recipes(cls):
        query = "DELETE FROM recipes;"
        results = connectToMySQL('my_kitchen_schema').query_db(query)
        return