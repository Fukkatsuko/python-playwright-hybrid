import allure
import pytest

from src.api.models.petstore.order_model import OrderModel
from src.api.models.petstore.pet_model import PetModel
from utils.generators import generate_petstore_pet, generate_petstore_order


@pytest.mark.api
@allure.feature("API: Store's orders")
@allure.story("Manage orders")
@pytest.mark.parametrize("quantity, expected_status", [
    (1, "placed"),  # Regular order
    (5, "placed"),  # Bulk order
])
class TestOrder:

    @allure.title("Successful creating and deleting an order wih new pet")
    def test_order_e2e(self, pet_api, order_api, user_api, quantity, expected_status):
        with allure.step("Preparation: creating a pet via API"):
            new_pet = generate_petstore_pet()
            response_pet_create = pet_api.create_pet(new_pet.model_dump(by_alias=True))
            assert response_pet_create.status_code == 200
            created_pet = PetModel(**response_pet_create.json())

        with allure.step("Create order"):
            new_order = generate_petstore_order(pet_id=created_pet.id, quantity=quantity, status=expected_status)
            response_order_create = order_api.create_order(new_order.model_dump(by_alias=True))
            assert response_order_create.status_code == 200
            order_id = response_order_create.json()["id"]

        with allure.step("Check created order"):
            response_order_check = order_api.get_order_by_id(order_id)
            assert response_order_check.status_code == 200

            created_order = OrderModel(**response_order_check.json())
            assert created_order.pet_id == created_pet.id
            assert created_order.status == expected_status
            assert created_order.quantity == quantity

        with allure.step("Delete created order"):
            response_order_delete = order_api.delete_order(created_order.id)
            assert response_order_delete.status_code == 200

        with allure.step("Check deleted order"):
            response_deleted_order = order_api.get_order_by_id(created_order.id)
            assert response_deleted_order.status_code == 404

        with allure.step("Logout"):
            user_api.logout_user()

        with allure.step("Check: request not possible after logout"):
            res = order_api.get_inventory()
            if res.status_code == 200:
                pytest.xfail("Swagger Petstore demo API doesn't validate auth for this endpoint")

            assert res.status_code == 401
