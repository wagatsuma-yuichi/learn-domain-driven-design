from typing import Dict, List, Optional
from uuid import UUID

from domain.entities.order import Order
from domain.repositories.order_repository import OrderCommandRepositoryInterface, OrderQueryRepositoryInterface


class InMemoryOrderCommandRepository(OrderCommandRepositoryInterface):
    """メモリ内注文コマンドリポジトリの実装"""
    
    def __init__(self):
        self.orders: Dict[UUID, Order] = {}
    
    def save(self, order: Order) -> Order:
        """注文を保存する"""
        self.orders[order.id] = order
        return order
    
    def update(self, order: Order) -> Order:
        """注文を更新する"""
        if order.id in self.orders:
            self.orders[order.id] = order
        return order
    
    def delete(self, order_id: UUID) -> None:
        """注文を削除する"""
        if order_id in self.orders:
            del self.orders[order_id]


class InMemoryOrderQueryRepository(OrderQueryRepositoryInterface):
    """メモリ内注文クエリリポジトリの実装"""
    
    def __init__(self):
        self.orders: Dict[UUID, Order] = {}
    
    def find_by_id(self, order_id: UUID) -> Optional[Order]:
        """IDで注文を検索する"""
        return self.orders.get(order_id)
    
    def find_all_by_customer_id(self, customer_id: UUID) -> List[Order]:
        """顧客IDで全ての注文を検索する"""
        return [order for order in self.orders.values() if order.customer_id == customer_id]
    
    def find_all(self) -> List[Order]:
        """全ての注文を取得する"""
        return list(self.orders.values())