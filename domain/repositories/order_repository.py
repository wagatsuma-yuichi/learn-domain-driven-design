from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from domain.entities.order import Order


class OrderCommandRepositoryInterface(ABC):
    """注文コマンドリポジトリのインターフェース"""
    
    @abstractmethod
    def save(self, order: Order) -> Order:
        """注文を保存する"""
        pass
    
    @abstractmethod
    def update(self, order: Order) -> Order:
        """注文を更新する"""
        pass
    
    @abstractmethod
    def delete(self, order_id: UUID) -> None:
        """注文を削除する"""
        pass


class OrderQueryRepositoryInterface(ABC):
    """注文クエリリポジトリのインターフェース"""
    
    @abstractmethod
    def find_by_id(self, order_id: UUID) -> Optional[Order]:
        """IDで注文を検索する"""
        pass
    
    @abstractmethod
    def find_all_by_customer_id(self, customer_id: UUID) -> List[Order]:
        """顧客IDで全ての注文を検索する"""
        pass
    
    @abstractmethod
    def find_all(self) -> List[Order]:
        """全ての注文を取得する"""
        pass