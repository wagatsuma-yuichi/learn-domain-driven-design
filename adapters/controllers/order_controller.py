from usecases.create_order import CreateOrderUseCase
import uuid

class OrderController:
    def __init__(self, create_order_use_case: CreateOrderUseCase):
        self.create_order_use_case = create_order_use_case
    
    def create_order(self, customer_id: str, items: list) -> dict:
        """
        注文作成のエンドポイント
        
        Args:
            customer_id: 顧客ID
            items: 商品IDと数量のリスト [{"product_id": "p1", "quantity": 2}, ...]
            
        Returns:
            作成された注文の情報
        """
        # 注文IDを生成
        order_id = str(uuid.uuid4())
        
        # ユースケースを実行
        order_aggregate = self.create_order_use_case.execute(order_id, customer_id, items)
        
        # レスポンスを作成
        return {
            "order_id": order_aggregate.order.order_id,
            "customer_id": order_aggregate.order.customer_id,
            "status": order_aggregate.order.status,
            "items": [
                {
                    "product_id": item.product_id,
                    "quantity": item.quantity
                }
                for item in order_aggregate.items
            ]
        } 