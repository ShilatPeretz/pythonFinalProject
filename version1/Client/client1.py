import socket


PORT = 6060
SERVER = "127.0.0.1"
END = True
global client

def client_socket(send_data):
    global END
    client.send(send_data.encode())
    if send_data.lower() == "bye":
        client.close()
        END = False
    else:
        data_receive = client.recv(1024).decode()
        print(f"{data_receive}")

def connect_to_server(username, password):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))
    user_details = username+":"+password
    client_socket(user_details)

