from src.api.clients.base_client import BaseClient


class ConduitClient(BaseClient):
    def __init__(self, base_url):
        super().__init__(base_url)
        self.users = UserModule(self)
        self.articles = ArticleModule(self)


class UserModule:

    def __init__(self, client):
        self.client = client

    def register_user(self, payload: dict):
        return self.client.post("/users", json=payload)

    def login(self, email, password):
        payload = {"user": {"email": email, "password": password}}
        response = self.client.post("/users/login", json=payload)

        if response.status_code == 200:
            token = response.json()["user"]["token"]
            self.client.session.headers.update({'Authorization': f'Token {token}'})
        return response

    def get_current_user(self):
        return self.client.get(f"/user")


class ArticleModule:

    def __init__(self, client):
        self.client = client

    def create_article(self, data):
        return self.client.post("/articles", json=data)

    def delete_article(self, slug):
        return self.client.delete(f"/articles/{slug}")

    def get_article(self, slug):
        return self.client.get(f"/articles/{slug}")

    def get_comments(self, slug):
        return self.client.get(f"/articles/{slug}/comments")
