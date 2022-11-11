from flask_app import app
import requests
from flask import render_template, redirect, request, jsonify, flash, session
from flask_app.controllers import ingredients
from flask_app.controllers import users
from flask_app.models.recipe import Recipe
from flask_app.models.ingredient import Ingredient
from flask_app.models.shopping_list import ShoppingList
from flask_app.models.user import User

import os

# Finds all the recipes from the database from the API call and displays for the user
@app.route('/recipes')
def show_recipe_suggestions():
    print("here are some recipes")
    recipe_search_results = Recipe.get_all_recipes()
    session['current_page'] = 'recipes'
    shopping_list = []
    if 'user_name' in session:
        data = {
            'user_id': session['user_id']
        }
        shopping_list = ShoppingList.get_shopping_list(data)
    return render_template('recipes.html',recipe_search_results=recipe_search_results, shopping_list=shopping_list)

# Directs the user to the single selected recipe
# Performs another API call to retrieve the full instructions
@app.route('/recipes/recipe/<int:recipe_id>')
def routing_to_recipe(recipe_id):
    api_key = os.environ.get("RECIPE_KEY")

    single_recipe = Recipe.get_one_recipe_by_id({'id': recipe_id})
    sp_id = single_recipe.spoonacular_id

    if single_recipe.instructions != None:
        print("going straight to recipe without API")
        ingredients_list = single_recipe.full_ingredient_list.split("//split_locate//")
        ingredients_list.pop()
        session['current_page'] = f'recipes/recipe/{recipe_id}'
        shopping_list = []
        if 'user_name' in session:
            data = {
                'user_id': session['user_id']
            }
            shopping_list = ShoppingList.get_shopping_list(data)
        return render_template('show_recipe_page.html',full_recipe=single_recipe, ingredients_list=ingredients_list,shopping_list=shopping_list)
    
    r = requests.get(f"https://api.spoonacular.com/recipes/{sp_id}/information?apiKey={api_key}")
    recipe_info = r.json()

    ingredient_list_and_amount = ""

    for item in recipe_info['extendedIngredients']:
        ingredient_list_and_amount += item['original'] + "//split_locate//"
        print(ingredient_list_and_amount)

    data = {
        'id': recipe_id,
        'instructions': recipe_info['instructions'],
        'cook_time': recipe_info['readyInMinutes'],
        'full_ingredient_list': ingredient_list_and_amount,
        'credit': recipe_info['creditsText']
    }
    Recipe.update_recipe(data)
    full_recipe = Recipe.get_one_recipe_by_id({'id': recipe_id})
    ingredients_list = full_recipe.full_ingredient_list.split("//split_locate//")
    ingredients_list.pop()
    print("here is a single recipe you selected")
    session['current_page'] = f'recipes/recipe/{recipe_id}'
    shopping_list = []
    if 'user_name' in session:
        data = {
            'user_id': session['user_id']
        }
        shopping_list = ShoppingList.get_shopping_list(data)
    return render_template('show_recipe_page.html',full_recipe=full_recipe, ingredients_list=ingredients_list,shopping_list=shopping_list)