from passlib.context import CryptContext


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash_password(new_password: str):
    hashed_password = pwd_context.hash(new_password)
    return hashed_password


def verifypassword(attempted_password, hashed_password):
    return pwd_context.verify(attempted_password, hashed_password)
