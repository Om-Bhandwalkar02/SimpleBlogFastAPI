from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash:
    @staticmethod
    def get_password_hash(pwd: str):
        return pwd_context.hash(pwd)
