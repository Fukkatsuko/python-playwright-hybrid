from src.api.clients.base_client import BaseClient


class OrderClient(BaseClient):
    def create_order(self, order_data: dict):
        return self.post("/store/order", json=order_data)

    def get_order_by_id(self, order_id: int):
        return self.get(f"/store/order/{order_id}")

    def get_inventory(self):
        return self.get("/store/inventory")

    def delete_order(self, order_id: int):
        return self.delete(f"/store/order/{order_id}")
