import socket
import threading

SERVER_IP = "127.0.0.1"
SERVER_PORT =6060
clients_usernames = []
clients_objects = []

# start the server going
def init_server():
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP,SERVER_PORT))
    server_socket.listen(5)
    print(" waiting for clients")
    return server_socket

# recive data from client
# send the given command to scapysniff.py
# if client's data saya "bye" disconnent the client
def client_session(client_object,username):
    while True:
        data = client_object.recv(1024).decode()
        if data.lower() == "bye":
            print(f" {username} is disconnected")
            client_object.close()
            break
        #only prints the given data
        print(username+" :",data )
        client_object.send("Ack".encode())


# recive client and for each start a new thread to handle the client
# TODO: add login check
def main():
    server_socket = init_server()
    while True:
        client_object ,client_IP =  server_socket.accept()
        #print the client that connected
        print(client_object)
        print(client_IP)
        #recv username + password
        user_details = (client_object.recv(1024).decode()).split(":")
        if(len(user_details)!=2):
            client_object.send("user details not in the right format".encode())
            continue
        username, password = user_details[0],user_details[1]
        ##TODO: check with data base
        clients_usernames.append(username)
        clients_objects.append(client_object)
        client_object.send("Welcome to Server".encode())
        client_th = threading.Thread(target=client_session, args=(client_object,username))
        client_th.start()


main()