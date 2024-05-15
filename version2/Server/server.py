#####################################################################################################################
# Import necessary libraries
import socket
import pickle
import threading
from scapysniff import sniff_packets
from DataBase.DbHandler.usersTable import search_user, add_new_user
from ftpCommand import init_ftp_server
from DataBase.DbHandler.usersTable import init

# server details
PORT = 12345
SERVER = "127.0.0.1"

# Initialize lists to store connected clients' usernames and objects
clients_usernames = []
clients_objects = []

# Start the server
def init_server():
    init()
    init_ftp_server()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER, PORT))
    server_socket.listen(5)
    print("Waiting for clients...")
    return server_socket

# Function to handle each client session
def client_session(client_object, username):
    while True:
        data = client_object.recv(1024).decode()
        if data.lower() == "bye":
            print(f"{username} is disconnected")
            client_object.close()
            break
        if not data :
            continue
        print(username + ":", data)
        # Sniff packets based on the received command
        packets_to_send = sniff_packets(data)
        print("Length of packets to send:", len(packets_to_send))

        # Serialize all objects in packets_to_send
        serialized_objects = [pickle.dumps(obj) for obj in packets_to_send]

        # Send each serialized object
        for serialized_data in serialized_objects:
            # Send the serialized object
            print("Serialized data:", serialized_data)
            client_object.send(serialized_data)
            client_object.recv(1024) # client sends ack to tell that first packet was recieved

        print("Data sent to client.")
        client_object.send("done".encode())

# Main function to accept client connections
def main():
    server_socket = init_server()
    while True:
        client_object, client_IP = server_socket.accept()
        print(f"Client connected: {client_IP}")
        # Receive username and password from the client
        user_details = (client_object.recv(1024).decode()).split(":")
        if len(user_details) != 3:
            client_object.send("User details not in the right format".encode())
            continue
        type_enter, username, password = user_details[0], user_details[1], user_details[2]
        # Check with database
        if type_enter == "register":
            add_new_user(username, password)
            client_object.send("New user added".encode())
        elif search_user(username, password):
            print("Username and password are correct:", username, password)
            clients_usernames.append(username)
            clients_objects.append(client_object)
            client_object.send("200 OK".encode())
            client_thread = threading.Thread(target=client_session, args=(client_object, username))
            client_thread.start()
        else:
            print("client is being released")
            client_object.send("Error: Client details are wrong".encode())

# Start the main function
if __name__ == "__main__":
    main()