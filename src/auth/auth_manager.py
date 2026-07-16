"""
auth_manager.py
Gestión básica de autenticación para ToDo.
Versión inicial.
"""

from dataclasses import dataclass
from hashlib import sha256
from secrets import token_hex
from datetime import datetime, timedelta


@dataclass
class User:
    username: str
    password_hash: str
    role: str = "user"
    enabled: bool = True


class AuthManager:

    def __init__(self):
        self.users = {}
        self.sessions = {}

    @staticmethod
    def hash_password(password: str) -> str:
        return sha256(password.encode("utf-8")).hexdigest()

    def add_user(self, username: str, password: str, role="user"):
        self.users[username] = User(
            username=username,
            password_hash=self.hash_password(password),
            role=role
        )

    def authenticate(self, username: str, password: str):
        user = self.users.get(username)
        if not user or not user.enabled:
            return None

        if user.password_hash != self.hash_password(password):
            return None

        token = token_hex(32)

        self.sessions[token] = {
            "user": username,
            "role": user.role,
            "expires": datetime.now() + timedelta(hours=8)
        }

        return token

    def validate_token(self, token: str):
        session = self.sessions.get(token)

        if not session:
            return None

        if session["expires"] < datetime.now():
            self.sessions.pop(token, None)
            return None

        return session

    def logout(self, token: str):
        return self.sessions.pop(token, None) is not None


if __name__ == "__main__":
    auth = AuthManager()
    auth.add_user("admin", "admin123", "admin")

    token = auth.authenticate("admin", "admin123")
    print("Token:", token)
    print(auth.validate_token(token))
