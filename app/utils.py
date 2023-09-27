from passlib.context import CryptContext

#hashing purposes 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password):
    return pwd_context.hash(password)

def verify(user_pass,actual_pass):
    return pwd_context.verify(user_pass,actual_pass)



