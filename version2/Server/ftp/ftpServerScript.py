from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


def start_ftp_server(server_running):
    authorizer = DummyAuthorizer()
    authorizer.add_user("myuser", "mypassword", r"C:\Users\97250\PycharmProjects\pythonFinalProject", perm="elradfmw")

    handler = FTPHandler
    handler.authorizer = authorizer

    server = FTPServer(("127.0.0.1", 21), handler)

    # Check if server should continue running
    while server_running.is_set():
        server.serve_forever(timeout=1, blocking=False)

def server_main(server_running):
    start_ftp_server(server_running)
