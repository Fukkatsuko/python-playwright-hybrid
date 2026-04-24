from src.api.clients.base_client import BaseClient


class PetClient(BaseClient):

    def get_pet_by_id(self, pet_id):
        return self.get(f"/pet/{pet_id}")

    def get_pet_by_status(self, status):
        params = {"status": status}
        return self.get("/pet/findByStatus", params=params)

    def create_pet(self, data):
        return self.post("/pet", json=data)

    def update_pet_with_form(self, pet_id, name, status):
        data = {"name": name, "status": status}
        return self.post(f"/pet/{pet_id}", data=data)

    def upload_image(self, pet_id, file_path):
        with open(file_path, 'rb') as img:
            files = {'file': img}
            return self.post(f"/pet/{pet_id}/uploadImage", files=files)

    def delete_pet(self, pet_id):
        return self.delete(f"/pet/{pet_id}")
