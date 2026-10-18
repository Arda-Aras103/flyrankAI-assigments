import os
from supabase import create_client


class AuthService:
    def __init__(self):
        self.client = create_client(
            os.getenv("SUPABASE_URL"),
            os.getenv("SUPABASE_KEY"),
        )

    def sign_up(self, email: str, password: str):
        return self.client.auth.sign_up({"email": email, "password": password})

    def sign_in(self, email: str, password: str):
        return self.client.auth.sign_in_with_password(
            {"email": email, "password": password}
        )

    def get_user(self, token: str):
        return self.client.auth.get_user(token)

    def sign_out(self):
        self.client.auth.sign_out()
