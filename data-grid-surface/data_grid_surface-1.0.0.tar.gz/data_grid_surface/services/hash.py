import hashlib
import base64

def sha256(password):
    """Hashes the string and returns that hash value

    Arguments:
    password -- password to be hashed
    """
    
    if not password or password == '':
        raise ValueError({ "Error": "Password does not exist or does not contain any character!" })
    
    try:
        return base64.b64encode(hashlib.sha256(password.encode('utf-8')).digest()).decode('utf-8')
    except Exception as e:
        raise ValueError({ "Error": "Some error occured during password hashing!" })