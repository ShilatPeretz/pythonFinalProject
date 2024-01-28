from flask import Flask, request, Blueprint, render_template, url_for, redirect
from Client.client1 import connect_to_server

app=Flask(__name__)

command_blueprint = Blueprint('auth', __name__)

@app.route('/login', methods=['GET','POST'])

def login():
    error=None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not connect_to_server(username, password):
            error="wrong user details please try agian"
        else:
            return redirect(url_for('main'))
    #TODO: write login html

    return render_template('login.html',error=error)

if __name__ == '__main__':
    app.run(debug=True)
