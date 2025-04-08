from datetime import datetime
from typing import List

class OrderItem:
    def __init__(self, product_id: str, quantity: int, order: 'Order'):
        self.product_id = product_id
        self.quantity = quantity
        self.order = order  # Orderへの参照

class Order:
    def __init__(self, order_id: str, customer_id: str):
        self.order_id = order_id  # 識別子 (不変)
        self.customer_id = customer_id
        self._status = "PENDING"
        self._version = 0  # 楽観的排他制御用
        self.items = []  # 注文アイテムのリスト
        self._pending_events = []  # ドメインイベントのリスト

    @property
    def status(self):
        return self._status

    def change_status(self, new_status: str):
        if self._status == "CANCELLED":
            raise ValueError("キャンセルされた注文は変更できません")
        self._status = new_status
        self._version += 1

    def add_item(self, product_id: str, quantity: int):
        item = OrderItem(product_id=product_id, quantity=quantity, order=self)
        self.items.append(item)
        return item

    def ship(self, tracking_number: str):
        from domain.events.order_events import OrderShippedEvent
        self.change_status("SHIPPED")
        self._pending_events.append(
            OrderShippedEvent(self.order_id, datetime.now(), tracking_number)
        )

    def get_pending_events(self):
        return self._pending_events.copy()  # コピーを返す

    def clear_events(self):
        self._pending_events.clear() 