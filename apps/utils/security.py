from passlib.context import CryptContext
from passlib.exc import UnknownHashError
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def validate_secret(secret, hash):
    try:
        return pwd_context.verify(secret, hash)
    except UnknownHashError:
        return False