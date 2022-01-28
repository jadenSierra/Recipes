import re
from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/recipe/create')
def recipe_create():
    if "id" not in session:
        return redirect("/")

    user = session["id"]

    return render_template("recipe_create.html", user = user)

@app.route('/recipe/create/new', methods = ['POST'])
def new_recipe():

    print(request.form)

    if not Recipe.validate_recipe(request.form):
        return redirect('/recipe/create')

    data = {
        **request.form
    }

    Recipe.save(data)

    return redirect("/dashboard") 

@app.route('/recipe/delete/<int:id>')
def destroy(id):

    data = {
        "id" : id
    }
    Recipe.destroy(data)
    return redirect("/dashboard")

@app.route('/recipe/instructions/<int:id>')
def view(id):

    if "id" not in session:
        return redirect("/dashboard")

    recipe_data = {
        "id" : id
    }

    user_data = {
        "id" : session["id"]
    }

    user = User.get_one(user_data)
    recipe = Recipe.get_one(recipe_data)

    return render_template("view.html", recipe = recipe, user = user )

@app.route('/recipe/edit/<int:id>')
def update(id):

    recipe_data = {
        "id" : id
    }

    recipe = Recipe.get_one(recipe_data)

    if session["id"] != recipe.user_id:
        return redirect("/dashboard")

    recipe_data = {
        "id" : id
    }

    user_data = {
        "id" : session['id']
    }

    user = User.get_one(user_data)
    recipe = Recipe.get_one(recipe_data)

    return render_template("edit.html", user = user, recipe = recipe)


@app.route('/recipe/update', methods = ['POST'])
def update_recipe():

    recipe_data = {
        "id" : request.form['recipe_id']
    }

    recipe = Recipe.get_one(recipe_data)

    if session["id"] != recipe.user_id:
        return redirect("/dashboard")


    if not Recipe.validate_recipe(request.form):
        return redirect(f'/recipe/edit/{recipe.id}')

    Recipe.update(request.form)

    return redirect("/dashboard")