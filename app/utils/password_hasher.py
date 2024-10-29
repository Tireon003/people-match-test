import bcrypt


class HashTool:

    @staticmethod
    def hash_password(password: str) -> str:
        hashed_password = (
            bcrypt.hashpw(
                password.encode('utf-8'),
                bcrypt.gensalt()
            )
            .decode('utf-8')
        )
        return hashed_password

    @staticmethod
    def check_password(password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            password=password.encode('utf-8'),
            hashed_password=hashed_password.encode('utf-8')
        )
