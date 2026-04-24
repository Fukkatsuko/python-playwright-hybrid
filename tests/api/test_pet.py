import allure
import pytest

from src.api.models.petstore.pet_model import PetModel
from utils.generators import generate_petstore_pet


@pytest.mark.api
@allure.feature("API: Pets")
@allure.story("Manage pets")
@pytest.mark.parametrize("pet_name, pet_status", [
    ('Darren', "pending"),
    ('Debit', "sold")])
class TestPet:

    @allure.title("Successful creating, updating and deleting new pet")
    def test_pet_lifecycle(self, pet_api, pet_name, pet_status):
        with allure.step("Creating new pet"):
            new_pet = generate_petstore_pet()
            response_create = pet_api.create_pet(new_pet.model_dump(by_alias=True))
            assert response_create.status_code == 200
            pet_id = response_create.json()["id"]

        with allure.step("Check created pet"):
            response_check_create = pet_api.get_pet_by_id(pet_id)
            assert response_check_create.status_code == 200

        with allure.step("Update pet"):
            response_update = pet_api.update_pet_with_form(pet_id, pet_name, pet_status)
            assert response_update.status_code == 200

        with allure.step("Check updated pet"):
            response_check = pet_api.get_pet_by_id(pet_id)
            updated_pet = PetModel(**response_check.json())
            assert response_check.status_code == 200
            assert updated_pet.name == pet_name
            assert updated_pet.status == pet_status

        with allure.step("Delete pet"):
            response_delete = pet_api.delete_pet(pet_id)
            assert response_delete.status_code == 200

        with allure.step("Check deleted pet"):
            response_check = pet_api.get_pet_by_id(pet_id)
            assert response_check.status_code == 404
