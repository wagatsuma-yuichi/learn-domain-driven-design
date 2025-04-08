from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from application.interfaces.dto import OrderDTO


class OrderCreationInputBoundary(ABC):
    """注文作成の責務を持つユースケース"""
    
    @abstractmethod
    def create_order(self, order_dto: OrderDTO) -> OrderDTO:
        """注文を作成する"""
        pass


class OrderQueryInputBoundary(ABC):
    """注文照会の責務を持つユースケース"""
    
    @abstractmethod
    def get_order(self, order_id: UUID) -> OrderDTO:
        """注文を取得する"""
        pass
    
    @abstractmethod
    def get_customer_orders(self, customer_id: UUID) -> List[OrderDTO]:
        """顧客の注文を取得する"""
        pass


class OrderManagementInputBoundary(ABC):
    """注文管理の責務を持つユースケース"""
    
    @abstractmethod
    def update_order_status(self, order_id: UUID, status: str) -> OrderDTO:
        """注文ステータスを更新する"""
        pass
    
    @abstractmethod
    def cancel_order(self, order_id: UUID) -> OrderDTO:
        """注文をキャンセルする"""
        pass


class OrderCreationOutputBoundary(ABC):
    """注文作成の出力境界"""
    
    @abstractmethod
    def present_created_order(self, order_dto: OrderDTO) -> None:
        """作成された注文を表示する"""
        pass


class OrderQueryOutputBoundary(ABC):
    """注文照会の出力境界"""
    
    @abstractmethod
    def present_order(self, order_dto: OrderDTO) -> None:
        """単一の注文を表示する"""
        pass
    
    @abstractmethod
    def present_orders(self, order_dtos: List[OrderDTO]) -> None:
        """注文リストを表示する"""
        pass


class OrderManagementOutputBoundary(ABC):
    """注文管理の出力境界"""
    
    @abstractmethod
    def present_updated_order(self, order_dto: OrderDTO) -> None:
        """更新された注文を表示する"""
        pass
    
    @abstractmethod
    def present_cancelled_order(self, order_dto: OrderDTO) -> None:
        """キャンセルされた注文を表示する"""
        pass


class OrderErrorOutputBoundary(ABC):
    """エラー出力の境界"""
    
    @abstractmethod
    def present_error(self, message: str) -> None:
        """エラーを表示する"""
        pass 


