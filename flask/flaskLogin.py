from flask import flask, request, jsonify, Blueprint, render_template

command_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods=['GET','POST'])

def login():
    #TODO:verify with DB
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
    #TODO: write login html

    return render_template('login.html')
