from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash, session



class ShoppingList:
    def __init__(self,data):
        self.id = data['id']
        self.item_name = data['item_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def add_item_to_shopping_list(cls,data):
        query = "INSERT INTO shopping_list (item_name, user_id) VALUES (%(item_name)s, %(user_id)s);"
        results = connectToMySQL('my_kitchen_schema').query_db(query,data)
        return results

    @classmethod
    def get_shopping_list(cls, data):
        query = "SELECT * FROM shopping_list WHERE user_id = %(user_id)s;"
        results = connectToMySQL('my_kitchen_schema').query_db(query,data)
        shoppping_list = []
        for item in results:
            shoppping_list.append(cls(item))
        return shoppping_list

    @classmethod
    def clear_shopping_list(cls,data):
        query = "DELETE FROM shopping_list WHERE user_id = %(user_id)s;"
        results = connectToMySQL('my_kitchen_schema').query_db(query,data)
        return results
    
    @classmethod
    def remove_item_from_shopping_list(cls,data):
        query = "DELETE FROM shopping_list WHERE id = %(id)s;"
        results = connectToMySQL('my_kitchen_schema').query_db(query,data)
        return results