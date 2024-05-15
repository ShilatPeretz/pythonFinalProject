import socket
import pickle

PORT = 12345
SERVER = "127.0.0.1"

global client
def connect_to_server(type_enter, user, password):
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((SERVER, PORT))
        message = f"{type_enter}:{user}:{password}"
        print("Sending message:", message)
        response = client_socket_send_message(message)
        print("Server response:", response)
        if response == "Error: Client details are wrong":
            return False
        return True
    except Exception as e:
        print("Error connecting to server:", e)
        client.close()  # Close the socket in case of an error
        return False, None

def client_socket_send_message(send_data):
    global client
    try:
        client.send(send_data.encode())
        if send_data.lower() == "bye":
            return ""  # Return an empty string if sending "bye"
        else:
            data_received = client.recv(1024).decode()
            return data_received
    except Exception as e:
        print("Error in client socket:", e)
        return ""

def client_socket_send_protocol(protocol_info):
    global client
    try:
        # Send protocol information to the server
        client.send(protocol_info.encode())

        received_objects = []
        tmp = []
        ####################################
        # Read the length of the serialized data
        while True:
            chunk = client.recv(4096)
            # print("chunk", chunk)
            if not chunk:
               raise ValueError("Connection closed by server")
            if chunk == "done".encode():
               break
            tmp.append(chunk)
            client.send("ack".encode())

        # Deserialize the received data using pickle and append to the list
        for packet in tmp:
            try:
                obj = pickle.loads(packet)
                received_objects.append(obj)
            except pickle.UnpicklingError as unpickle_err:
                print("Error: Failed to unpickle the received data:", unpickle_err)
                print("Serialized data received:", packet)
    finally:
        print("done")

    return received_objects


def disconnect_client():
    global client
    client.send("bye".encode())
    client.close()
####################################

