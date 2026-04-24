from src.api.clients.base_client import BaseClient


class UserClient(BaseClient):
    def create_user(self, user_data):
        return self.post("/user", json=user_data)

    def get_user_by_name(self, username):
        return self.get(f"/user/{username}")

    def delete_user(self, username):
        return self.delete(f"/user/{username}")

    def logout_user(self):
        self.get("/user/logout")
        self.logout()
