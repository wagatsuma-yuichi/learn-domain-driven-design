from domain.entities.order import Order
from domain.aggregates.order_aggregate import OrderAggregate
from domain.repositories.order_repository import OrderRepository
from domain.services.inventory_service import InventoryService

class CreateOrderUseCase:
    def __init__(self, order_repository: OrderRepository, inventory_service: InventoryService):
        self.order_repository = order_repository
        self.inventory_service = inventory_service
        
    def execute(self, order_id: str, customer_id: str, items: list) -> OrderAggregate:
        """
        注文を作成するユースケース
        
        Args:
            order_id: 注文ID
            customer_id: 顧客ID
            items: 商品IDと数量のリスト [{"product_id": "p1", "quantity": 2}, ...]
            
        Returns:
            作成された注文集約
        """
        # 注文エンティティを作成
        order = Order(order_id, customer_id)
        
        # 注文集約を作成
        order_aggregate = OrderAggregate(order, [])
        
        # 商品を追加
        for item in items:
            order_aggregate.add_item(item["product_id"], item["quantity"])
        
        # 在庫の確認と割り当て
        self.inventory_service.allocate(order)
        
        # リポジトリに保存
        self.order_repository.save(order_aggregate)
        
        return order_aggregate 