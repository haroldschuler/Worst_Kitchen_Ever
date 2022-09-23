from flask_app import app
import requests
from flask import render_template, redirect, request, jsonify, flash, session
from flask_app.controllers import recipes
from flask_app.controllers import users
from flask_app.models.recipe import Recipe
from flask_app.models.ingredient import Ingredient
from flask_app.models.shopping_list import ShoppingList
from flask_app.models.user import User

@app.route('/')
def show_search_page():
    print("ready to find some recipes")
    Recipe.delete_recipes()
    session['current_page'] = '/'
    shopping_list = []
    if 'user_name' in session:
        data = {
            'user_id': session['user_id']
        }
        shopping_list = ShoppingList.get_shopping_list(data)
    return render_template('search_page.html',shopping_list=shopping_list)

@app.route('/search_ingredients', methods=['POST'])
def search_database_for_ingredients():
    # print(request.form['value'])
    data = {
        'ingredient_name': '%%' + request.form['value'] + '%%'
    }
    search_results = Ingredient.search_ingredients_by_text(data)
    json_package = {}
    # json_package['list'] = []
    counter = 1
    for item in search_results:
        json_package[f"item{counter}"] = {'id': item.id,'ingredient_name': item.ingredient_name}
        # json_package['list'][counter] = {'id': item.id,'ingredient_name': item.ingredient_name}
        counter += 1
    if json_package == {}:
        json_package['item1'] = {'id': "none",'ingredient_name': "none"}
    json_package['counter'] = counter - 1
    # print(json_package)
    # print(search_results)
    # print(search_results[0])
    # print(search_results[0].name)
    return jsonify(json_package)

@app.route('/find_recipes', methods=['POST'])
def find_recipes():
    print("finding recipes....")
    api_key = '1259ebb6297343a79a643091713a9e79'
    number = 3
    ranking = 1
    data = {
        **request.form
    }
    print(request.form)
    ingredient_string = ""
    if len(data) == 0:
        flash('Must select at least 1 ingredient','search_error')
        return redirect('/')
    else:
        ingredient_string = ",".join(data)

    print(ingredient_string)

    r = "not_practice"
    if r == "practice":
        data = {
            'spoonacular_id': 73420,
            'recipe_name': "Apple Strudel",
            'image_link': "https://spoonacular.com/recipeImages/73420-312x231.jpg",
            'missed_ingredients': "garlic, cheese",
        }
        # Recipe.create_recipe(data)
        return redirect('/recipes')

    r = requests.get(f"https://api.spoonacular.com/recipes/findByIngredients?apiKey={api_key}&ingredients={ingredient_string}&number={number}&ranking={ranking}")
    recipes = r.json()
    # print(recipes)
    for recipe in recipes:
        print(recipe)
        missing_ingredients = ""
        for missed_ing in recipe['missedIngredients']:
            missing_ingredients = missing_ingredients + missed_ing['name'] + ","
        print(missing_ingredients)
        data = {
            'spoonacular_id': recipe['id'],
            'recipe_name': recipe['title'],
            'image_link': recipe['image'],
            'missed_ingredients': missing_ingredients
        }
        Recipe.create_recipe(data)
    return redirect('/recipes')

@app.route('/back_to_search', methods=['POST'])
def back_to_search():
    return redirect('/')

@app.route('/back_to_recipes', methods=['POST'])
def back_to_recipes():
    return redirect('/recipes')

@app.route('/clear_shopping_list', methods=['POST'])
def clear_list():
    data = {
        'user_id': session['user_id']
    }
    ShoppingList.clear_shopping_list(data)
    return redirect(f'/{session["current_page"]}')

@app.route('/recipes/add_to_shopping_list', methods=['POST'])
def add_item_to_shopping_list():
    if 'user_id' not in session:
        return jsonify(message="user must log in to add items")
    data = {
        'item_name': request.form['item'],
        'user_id': session['user_id']
    }
    ShoppingList.add_item_to_shopping_list(data)
    return jsonify(message="item added")

@app.route('/recipes/remove_from_shopping_list', methods=['POST'])
def remove_item_from_shopping_list():
    data = {
        'id': request.form['item_id']
    }
    ShoppingList.remove_item_from_shopping_list(data)
    return jsonify(message="item removed")