from ftplib import FTP

def upload_file():
    ftp = FTP("127.0.0.1")
    ftp.login(user="myuser", passwd="mypassword")
    ftp.cwd("..")

    file_path = r"C:\Users\97250\PycharmProjects\pythonFinalProject\version2\Server\ftp\hello.txt"
    with open(file_path, "rb") as file:
        ftp.storbinary("STOR file_to_upload.txt", file)

    ftp.quit()


def client_main():
    upload_file()