from flask import Flask, request, Blueprint, render_template, jsonify
from version2.Client.client import connect_to_server, client_socket_send_protocol, disconnect_client
from version2.Client.HashMD5 import get_hash
import ipapi


# change when working on another computer!
CLIENT_IP = '192.168.56.1'
server_socket = None



# app
app=Flask(__name__)
command_blueprint = Blueprint('auth', __name__)

# initial page - home page
@app.route('/')
def EnterSite():
    #connect_to_server('login', "username", "password")
    return render_template('login.html', error="none")

# login page
@app.route('/login', methods=['GET','POST'])
def login():
    type_enter = "login"
    error="none"
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(f"username: {username}, password {password}")
        hash_password = get_hash(password)
        if not connect_to_server(type_enter, username, hash_password):
            print("could not log in")
            error="wrong user details please try agian"
            return render_template('login.html', error=error)
        else:
            return render_template('main.html')

    return render_template('login.html',error=error)

# register page
@app.route('/register', methods=['GET','POST'])
def register():
    type_enter = "register"
    error="none"
    if request.method == 'POST':
        username = request.form.get('username')
        print(username)
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if (password2 != password1):
            return render_template('register.html', error="the passwords don't match")
        if (len(password1)<8):
            return render_template('register.html', error="password length should be at least 8")
        hash_password = get_hash(password1)
        if not connect_to_server(type_enter, username, hash_password):
            error="something is wrong with the server :("
        else:
            return render_template('main.html')
    # a get request
    return render_template('register.html', error=error)


@app.route('/main')
def main():
    return render_template('main.html')


@app.route('/http', methods=['GET','POST'])
def http():
    site = request.form.get('site_name')
    protocol_info = "http:"+site
    result_packets = client_socket_send_protocol(protocol_info)
    print("the lennnn:", result_packets)
    return render_template('result.html', packets=result_packets, command="http")


@app.route('/ftp', methods=['GET','POST'])
def ftp():
    protocol_info = "ftp:ftp"
    result_packets = client_socket_send_protocol(protocol_info)
    print("the lennnn:",result_packets)
    return render_template('result.html', packets=result_packets, command = "ftp")


@app.route('/tracert', methods=['GET','POST'])
def tracert():
    ip_address = request.form.get('ip_address')
    protocol_info = "tracert:"+ip_address
    result_packets = client_socket_send_protocol(protocol_info)
    return render_template('result.html', packets = result_packets, command = "tracert")


@app.route('/disconnect', methods=['GET','POST'])
def disconnect():
    disconnect_client()
    return render_template('login.html', error = "none")

#######################################
# locate the ip details using ipapi
@app.route('/locate_ip', methods=['GET'])
def locate_ip():
    # Get the IP address from the request
    ip_address = request.args.get('ip')

    # Call the function to locate the IP address
    geolocation_data = ipapi.location(ip_address)

    print(geolocation_data)
    # Return the geolocation data as JSON response
    return jsonify(geolocation_data)
#####################################




if __name__ == '__main__':
    app.run(debug=True)


