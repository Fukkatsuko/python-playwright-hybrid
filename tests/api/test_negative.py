import allure
import pytest


@pytest.mark.api
@allure.feature("API: Negative test for PetStore")
@allure.story("Negative ID tests")
@pytest.mark.parametrize("bad_id", [
    "abc",
    "!@#$",
    " ",
    "fdf12313"
])
class TestNegativeId:

    @allure.title("Pet search by an unauthorized user")
    def test_get_pet_by_unauthorized_user(self, un_auth_pet_api, bad_id):
        with allure.step("Check pet"):
            response_pet = un_auth_pet_api.get_pet_by_id(bad_id)
            assert response_pet.status_code in [400, 404, 401]

    @allure.title("Search for a non-existent pet")
    def test_get_not_existing_pet(self, pet_api, bad_id):
        with allure.step("Check a non-existent pet"):
            response_pet = pet_api.get_pet_by_id(bad_id)

            if bad_id == " " and response_pet.status_code == 200:
                pytest.xfail("API bug: search with empty string returns 200")

            assert response_pet.status_code in [400, 404]

            if response_pet.status_code == 404:
                error_data = response_pet.json()
                if "java.lang" not in error_data.get("message", ""):
                    assert "Pet not found" in error_data.get("message", "")

    @allure.title("Search for a non-existent order")
    def test_get_not_existing_order(self, order_api, bad_id):
        with allure.step("Check a non-existent order"):
            response_order = order_api.get_order_by_id(bad_id)
            assert response_order.status_code in [400, 404]

    @allure.title("Creating an order with a non-existent pet")
    def test_create_order_with_not_existing_pet(self, order_api, bad_id):
        with allure.step("Create order with a non-existent pet"):
            payload = {"petId": bad_id, "quantity": 1, "status": "placed"}
            response = order_api.post("/store/order", json=payload)

            if bad_id == " " and response.status_code == 200:
                pytest.xfail("API bug: allows empty string ID for orders")

            assert response.status_code in [400, 404, 500]


@pytest.mark.api
@allure.feature("API: Negative test for PetStore")
@allure.story("Negative Logic tests")
class TestNegativeLogic:

    @allure.title("Creating a pet with an empty name")
    def test_create_pet_with_empty_name(self, pet_api):
        with allure.step("Send request with empty name"):
            payload = {"name": "", "status": "available"}
            response = pet_api.create_pet(payload)

            if response.status_code == 200:
                pytest.xfail("Bug: Server allows creating a pet with an empty name")

            assert response.status_code in [400, 405]

    @allure.title("Delete non-existent pet")
    def test_delete_non_existent_pet(self, pet_api):
        with allure.step("Delete pet with ID 0"):
            response = pet_api.delete_pet(0)
            assert response.status_code == 404
