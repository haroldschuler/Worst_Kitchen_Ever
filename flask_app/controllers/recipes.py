from flask_app import app
import requests
from flask import render_template, redirect, request, jsonify, flash, session
from flask_app.controllers import ingredients
from flask_app.controllers import users
from flask_app.models.recipe import Recipe
from flask_app.models.ingredient import Ingredient
from flask_app.models.shopping_list import ShoppingList
from flask_app.models.user import User

@app.route('/recipes')
def show_recipe_suggestions():
    print("here are some recipes")
    recipe_search_results = Recipe.get_all_recipes()
    # missing_ingredients = recipe_search_results.missed_ingredients.split(",")
    # missing_ingredients = recipe_search_results.missed_ingredients
    print(recipe_search_results[0].missed_ingredients)
    print(recipe_search_results[1].missed_ingredients)
    print(recipe_search_results[2].missed_ingredients)
    # print(recipe_search_results[0].recipe_name)
    # print(recipe_search_results[0].missed_ingredients)
    # print(recipe_search_results[0].image_link)
    session['current_page'] = 'recipes'
    shopping_list = []
    if 'user_name' in session:
        data = {
            'user_id': session['user_id']
        }
        shopping_list = ShoppingList.get_shopping_list(data)
    return render_template('recipes.html',recipe_search_results=recipe_search_results, shopping_list=shopping_list)

@app.route('/recipes/recipe/<int:recipe_id>')
def routing_to_recipe(recipe_id):
    api_key = '1259ebb6297343a79a643091713a9e79'

    single_recipe = Recipe.get_one_recipe_by_id({'id': recipe_id})
    sp_id = single_recipe.spoonacular_id

    r = "not_practice"
    if r == "practice":
        data = {
            'id': recipe_id,
            'instructions': "add a thing, add thing 2, do thing 3",
            'cook_time': 60,
            'full_ingredient_list': "1 cup almonds//split_locate//1/2 cup milk//split_locate//2 eggs",
            'credit': "harold's recipe hut"
            }
        Recipe.update_recipe(data)
        full_recipe = Recipe.get_one_recipe_by_id({'id': recipe_id})
        print(full_recipe.full_ingredient_list)
        ingredients_list = full_recipe.full_ingredient_list.split("//split_locate//")
        print(ingredients_list)
        return render_template('show_recipe_page.html',full_recipe=full_recipe, ingredients_list=ingredients_list)

    # this can be commented out for actual use
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
    print(recipe_info)

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