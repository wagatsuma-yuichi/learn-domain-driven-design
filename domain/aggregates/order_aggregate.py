from typing import List
from datetime import datetime

from domain.entities.order import Order, OrderItem
from domain.events.order_events import OrderItemAddedEvent, OrderShippedEvent

class OrderAggregate:
    def __init__(self, order: Order, items: list[OrderItem]):
        self.order = order
        self.items = items
        self._domain_events = []  # ドメインイベントのリスト

    def add_item(self, product_id: str, quantity: int):
        if self.order.status != "PENDING":
            raise ValueError("確定済みの注文は変更できません")

        new_item = self.order.add_item(product_id, quantity)
        self.items.append(new_item)
        self._domain_events.append(OrderItemAddedEvent(product_id, quantity))

    def get_events(self):
        # 集約内のイベントと、オーダー自体のイベントを結合
        all_events = self._domain_events.copy()
        all_events.extend(self.order.get_pending_events())
        return all_events

    def ship(self, tracking_number: str):
        self.order.ship(tracking_number)
        self._domain_events.append(OrderShippedEvent(self.order.order_id, datetime.now(), tracking_number)) 