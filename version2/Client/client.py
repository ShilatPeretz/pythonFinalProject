from version2.Additional.data import PORT, SERVER, MSG_LENGTH
import socket
import pickle
from version2.classes.HttpPacketsClass import HttpPacket
from version2.classes.TracertPacketClass import TracertPacket
from version2.classes.FtpPacketsClass import FtpPacket

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
        if response == "error: client details are wrong":
            return False, client
        return True, client
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
            data_received = client.recv(MSG_LENGTH).decode()
            return data_received
    except Exception as e:
        print("Error in client socket:", e)
        return ""

def client_socket_send_protocol(protocol, protocol_info):
    global client
    try:
        # Send protocol information to the server
        client.send(protocol.encode())

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
                obj.print_packet()
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



def main():
    connected, client = connect_to_server('login', "username", "password")
    if connected:
        try:
            while True:
                protocol = input("Enter protocol to send: ")
                if protocol.lower() == "bye":
                    client.send("bye".encode())
                    break
                client_socket_send_protocol(protocol, "some info")  # Send protocol to server
        finally:
            client.close()

if __name__ == "__main__":
    main()
