from typing import Dict, List, Any

from application.interfaces.dto import OrderDTO
from application.interfaces.order_use_case import (
    OrderCreationOutputBoundary,
    OrderQueryOutputBoundary,
    OrderManagementOutputBoundary,
    OrderErrorOutputBoundary
)
from presentation.viewmodels.order_view_model import OrderViewModel


class BasePresenter:
    """基本プレゼンター"""
    
    def __init__(self):
        self.view_model = OrderViewModel()
    
    def present_error(self, message: str) -> None:
        """エラーを表示する"""
        self.view_model.set_error(message)
    
    def _to_dict(self, order_dto: OrderDTO) -> Dict[str, Any]:
        """OrderDTOを辞書に変換する"""
        return {
            "id": str(order_dto.id) if order_dto.id else None,
            "customer_id": str(order_dto.customer_id) if order_dto.customer_id else None,
            "items": [
                {
                    "product_id": str(item.product_id),
                    "quantity": item.quantity,
                    "price_per_unit": item.price_per_unit,
                    "total_price": item.quantity * item.price_per_unit
                }
                for item in order_dto.items
            ],
            "status": order_dto.status,
            "created_at": order_dto.created_at.isoformat() if order_dto.created_at else None,
            "updated_at": order_dto.updated_at.isoformat() if order_dto.updated_at else None,
            "total_amount": order_dto.total_amount or sum(item.quantity * item.price_per_unit for item in order_dto.items)
        }


class OrderCreationPresenter(BasePresenter, OrderCreationOutputBoundary, OrderErrorOutputBoundary):
    """注文作成プレゼンターの実装"""
    
    def present_created_order(self, order_dto: OrderDTO) -> None:
        """作成された注文を表示する"""
        order_data = self._to_dict(order_dto)
        self.view_model.set_order(order_data)


class OrderQueryPresenter(BasePresenter, OrderQueryOutputBoundary, OrderErrorOutputBoundary):
    """注文照会プレゼンターの実装"""
    
    def present_order(self, order_dto: OrderDTO) -> None:
        """単一の注文を表示する"""
        order_data = self._to_dict(order_dto)
        self.view_model.set_order(order_data)
    
    def present_orders(self, order_dtos: List[OrderDTO]) -> None:
        """注文リストを表示する"""
        orders_data = [self._to_dict(order_dto) for order_dto in order_dtos]
        self.view_model.set_orders(orders_data)


class OrderManagementPresenter(BasePresenter, OrderManagementOutputBoundary, OrderErrorOutputBoundary):
    """注文管理プレゼンターの実装"""
    
    def present_updated_order(self, order_dto: OrderDTO) -> None:
        """更新された注文を表示する"""
        order_data = self._to_dict(order_dto)
        self.view_model.set_order(order_data)
    
    def present_cancelled_order(self, order_dto: OrderDTO) -> None:
        """キャンセルされた注文を表示する"""
        order_data = self._to_dict(order_dto)
        self.view_model.set_order(order_data) 