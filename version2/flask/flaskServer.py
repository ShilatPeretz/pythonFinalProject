from flask import Flask, request, Blueprint, render_template, url_for, redirect
from version2.Client.client import connect_to_server, client_socket_send_protocol, disconnect_client


from version2.classes.HttpPacketsClass import HttpPacket
from version2.classes.TracertPacketClass import TracertPacket
from version2.classes.FtpPacketsClass import FtpPacket


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
    return render_template('login.html')

# login page
@app.route('/login', methods=['GET','POST'])
def login():
    type_enter = "login"
    error=None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not connect_to_server(type_enter, username, password):
            print("could not log in")
            error="wrong user details please try agian"
        else:
            return render_template('main.html')

    return render_template('login.html',error=error)

# register page
@app.route('/register', methods=['GET','POST'])
def register():
    type_enter = "register"
    error=None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not connect_to_server(type_enter, username, password):
            error="wrong user details please try agian"
        else:
            return redirect(url_for('main'))
    return render_template('login.html',error=error)

@app.route('/http', methods=['GET','POST'])
def http():
    site = "facebook.com"
    protocol_info = "http:"+site
    result_packets = client_socket_send_protocol("http", protocol_info)
    print("the lennnn:", result_packets)
    return render_template('result.html', packets=result_packets, command="http")


@app.route('/ftp', methods=['GET','POST'])
def ftp():
    protocol_info = "ftp:ftp"
    result_packets = client_socket_send_protocol("ftp", protocol_info)
    print("the lennnn:",result_packets)
    return render_template('result.html', packets=result_packets, command = "ftp")

@app.route('/tracert', methods=['GET','POST'])
def tracert():
    ip_address = "192.66.52.78"
    protocol_info = "tracert:"+ip_address
    result_packets = client_socket_send_protocol("tracert",protocol_info)
    return render_template('result.html', packets = result_packets, command = "tracert")

@app.route('/disconnect', methods=['GET','POST'])
def disconnect():
    disconnect_client()
    return render_template('login.html')




if __name__ == '__main__':
    app.run(debug=True)


