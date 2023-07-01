from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def validate_secret(secret, hash):
    return pwd_context.verify(secret, hash)