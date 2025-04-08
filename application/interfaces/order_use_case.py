from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from application.interfaces.dto import OrderDTO


class OrderCommandInputBoundary(ABC):
    """注文コマンド操作のインプットポート"""
    
    @abstractmethod
    def create_order(self, order_dto: OrderDTO) -> OrderDTO:
        """注文を作成する"""
        pass
    
    @abstractmethod
    def update_order_status(self, order_id: UUID, status: str) -> OrderDTO:
        """注文ステータスを更新する"""
        pass
    
    @abstractmethod
    def cancel_order(self, order_id: UUID) -> OrderDTO:
        """注文をキャンセルする"""
        pass


class OrderQueryInputBoundary(ABC):
    """注文クエリ操作のインプットポート"""
    
    @abstractmethod
    def get_order(self, order_id: UUID) -> OrderDTO:
        """注文を取得する"""
        pass
    
    @abstractmethod
    def get_customer_orders(self, customer_id: UUID) -> List[OrderDTO]:
        """顧客の注文を取得する"""
        pass


class OrderCommandOutputBoundary(ABC):
    """注文コマンド操作の出力境界"""
    
    @abstractmethod
    def present_created_order(self, order_dto: OrderDTO) -> None:
        """作成された注文を表示する"""
        pass
    
    @abstractmethod
    def present_updated_order(self, order_dto: OrderDTO) -> None:
        """更新された注文を表示する"""
        pass
    
    @abstractmethod
    def present_cancelled_order(self, order_dto: OrderDTO) -> None:
        """キャンセルされた注文を表示する"""
        pass


class OrderQueryOutputBoundary(ABC):
    """注文クエリ操作の出力境界"""
    
    @abstractmethod
    def present_order(self, order_dto: OrderDTO) -> None:
        """注文を表示する"""
        pass
    
    @abstractmethod
    def present_orders(self, order_dtos: List[OrderDTO]) -> None:
        """注文リストを表示する"""
        pass


class OrderErrorOutputBoundary(ABC):
    """注文操作のエラー出力境界"""
    
    @abstractmethod
    def present_error(self, message: str) -> None:
        """エラーを表示する"""
        pass


