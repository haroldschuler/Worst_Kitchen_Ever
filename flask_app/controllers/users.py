from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.controllers import recipes
from flask_app.controllers import ingredients
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_app.models.ingredient import Ingredient
from flask_app.models.shopping_list import ShoppingList

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/go_to_sign_up', methods=['POST'])
def going_to_sign_up():
    return redirect('/sign_up')

@app.route('/sign_up')
def sign_up_page():
    if 'user_id' in session:
        del session['user_id']
        del session['user_name']
    return render_template('sign_up.html')

@app.route('/registering', methods=['POST'])
def registering():
    answers = request.form
    if not User.validate_registration(answers):
        return redirect('/sign_up')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash
    }
    new_user = User.register_user(data)
    print("the new user id is", new_user)
    session['user_id'] = new_user
    user_id = {
        'id': new_user
    }
    session['user_name'] = User.get_user_from_id(user_id).first_name
    print("the new user's name is " + session['user_name'] + " and is logged in session")
    return redirect(f'/{session["current_page"]}')
    # return redirect('/')

@app.route('/go_to_login', methods=['POST'])
def going_to_login():
    return redirect('/login')

@app.route('/login')
def login_page():
    if 'user_id' in session:
        del session['user_id']
        del session['user_name']
    return render_template('login.html')

@app.route('/logging_in', methods=['POST'])
def logging_in():
    data = {
        'email': request.form['email2'],
        'password': request.form['password2']
    }
    if not User.validate_login(data):
        return redirect('/login')
    
    return redirect(f'/{session["current_page"]}')
    # return redirect('/')


@app.route('/logging_out', methods=['POST'])
def logging_out():
    if 'user_id' in session:
        del session['user_id']
        del session['user_name']
    return redirect(f'/{session["current_page"]}')
    # return redirect('/')