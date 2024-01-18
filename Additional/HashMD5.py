import hashlib


def get_hash(str):
    pas = str
    hashed_password = hashlib.md5(pas.encode()).hexdigest()
    print(hashed_password)
    return hashed_password