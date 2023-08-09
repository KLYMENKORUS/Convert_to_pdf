from passlib.context import CryptContext


class Hasher:

    password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def get_hashed_pass(cls, password: str) -> str:
        return cls.password_context.hash(password)

    @classmethod
    def verify_password(cls, password: str, hashed_pass: str) -> bool:
        return cls.password_context.verify(password, hashed_pass)