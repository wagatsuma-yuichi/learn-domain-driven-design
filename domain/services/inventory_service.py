from domain.entities.order import Order

class InventoryService:
    def __init__(self, repository):
        self.repository = repository

    def allocate(self, order: Order) -> None:
        for item in order.items:
            if not self.repository.has_stock(item.product_id, item.quantity):
                raise ValueError(f"{item.product_id}の在庫が不足しています")
            self.repository.reserve(item.product_id, item.quantity) 