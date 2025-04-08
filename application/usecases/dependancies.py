from fastapi import Depends
from typing import Annotated
from fastapi import status
from application.interfaces.order_use_case import (
    OrderCommandInputBoundary,
    OrderCommandOutputBoundary,
    OrderQueryInputBoundary,
    OrderQueryOutputBoundary,
    OrderErrorOutputBoundary
)
from application.interfaces.dto import OrderDTO
from presentation.viewmodels.order_view_model import HttpResponseOrderCreationViewModel
from infrastructure.repositories.in_memory_order_repository import (
    InMemoryOrderCommandRepository,
    InMemoryOrderQueryRepository
)
from application.usecases.order_interactor import (
    OrderCommandInteractor,
    OrderQueryInteractor
)
from domain.repositories.customer_repository import CustomerRepository
from domain.repositories.product_repository import ProductRepository
from infrastructure.repositories.in_memory_customer_repository import InMemoryCustomerRepository
from infrastructure.repositories.in_memory_product_repository import InMemoryProductRepository

def get_order_command_presenter() -> OrderCommandOutputBoundary:
    """注文コマンド用プレゼンターを提供"""
    return HttpResponseOrderCommandPresenter()

def get_order_query_presenter() -> OrderQueryOutputBoundary:
    """注文クエリ用プレゼンターを提供"""
    return HttpResponseOrderQueryPresenter()


def get_error_presenter() -> OrderErrorOutputBoundary:
    """エラー用プレゼンターを提供"""
    return HttpResponseOrderCommandPresenter()

def get_customer_repository() -> CustomerRepository:
    """顧客リポジトリを提供"""
    return InMemoryCustomerRepository()

def get_product_repository() -> ProductRepository:
    """製品リポジトリを提供"""
    return InMemoryProductRepository()

def get_order_command_repository():
    """注文コマンドリポジトリを提供"""
    return InMemoryOrderCommandRepository()

def get_order_query_repository():
    """注文クエリリポジトリを提供"""
    return InMemoryOrderQueryRepository()

class HttpResponseOrderCommandPresenter(OrderCommandOutputBoundary, OrderErrorOutputBoundary):
    """注文コマンド結果をHTTPレスポンス用に変換するプレゼンター"""
    
    def __init__(self):
        self.view_model = HttpResponseOrderCreationViewModel()
    
    def present_created_order(self, order_dto: OrderDTO) -> None:
        """作成された注文を表示する"""
        self.view_model = HttpResponseOrderCreationViewModel(status.HTTP_201_CREATED)
        order_data = self._to_dict(order_dto)
        self.view_model.set_body(order_data)
        if order_dto.id:
            self.view_model.add_header("Location", f"/orders/{order_dto.id}")
    
    def present_updated_order(self, order_dto: OrderDTO) -> None:
        """更新された注文を表示する"""
        self.view_model = HttpResponseOrderCreationViewModel(status.HTTP_200_OK)
        order_data = self._to_dict(order_dto)
        self.view_model.set_body(order_data)
    
    def present_cancelled_order(self, order_dto: OrderDTO) -> None:
        """キャンセルされた注文を表示する"""
        self.view_model = HttpResponseOrderCreationViewModel(status.HTTP_200_OK)
        order_data = self._to_dict(order_dto)
        self.view_model.set_body(order_data)
    
    def present_error(self, message: str) -> None:
        """エラーを表示する"""
        self.view_model = HttpResponseOrderCreationViewModel(status.HTTP_400_BAD_REQUEST)
        self.view_model.set_error(message)
    
    def _to_dict(self, order_dto: OrderDTO) -> dict:
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


class HttpResponseOrderQueryPresenter(OrderQueryOutputBoundary, OrderErrorOutputBoundary):
    """注文クエリ結果をHTTPレスポンス用に変換するプレゼンター"""
    
    def __init__(self):
        self.view_model = HttpResponseOrderCreationViewModel()
    
    def present_order(self, order_dto: OrderDTO) -> None:
        """単一の注文を表示する"""
        self.view_model = HttpResponseOrderCreationViewModel(status.HTTP_200_OK)
        order_data = self._to_dict(order_dto)
        self.view_model.set_body(order_data)
    
    def present_orders(self, order_dtos: list[OrderDTO]) -> None:
        """注文リストを表示する"""
        self.view_model = HttpResponseOrderCreationViewModel(status.HTTP_200_OK)
        orders_data = [self._to_dict(order_dto) for order_dto in order_dtos]
        self.view_model.set_body(orders_data)
    
    def present_error(self, message: str) -> None:
        """エラーを表示する"""
        self.view_model = HttpResponseOrderCreationViewModel(status.HTTP_400_BAD_REQUEST)
        self.view_model.set_error(message)
    
    def _to_dict(self, order_dto: OrderDTO) -> dict:
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


def order_command_usecase(
    order_repo: Annotated[InMemoryOrderCommandRepository, Depends(get_order_command_repository)],
    customer_repo: Annotated[CustomerRepository, Depends(get_customer_repository)],
    product_repo: Annotated[ProductRepository, Depends(get_product_repository)],
    presenter: Annotated[OrderCommandOutputBoundary, Depends(get_order_command_presenter)],
    error_presenter: Annotated[OrderErrorOutputBoundary, Depends(get_error_presenter)]
) -> OrderCommandInputBoundary:
    """注文コマンド用ユースケースを提供"""
    return OrderCommandInteractor(order_repo, customer_repo, product_repo, presenter, error_presenter)


def order_query_usecase(
    order_repo: Annotated[InMemoryOrderQueryRepository, Depends(get_order_query_repository)],
    presenter: Annotated[OrderQueryOutputBoundary, Depends(get_order_query_presenter)],
    error_presenter: Annotated[OrderErrorOutputBoundary, Depends(get_error_presenter)]
) -> OrderQueryInputBoundary:
    """注文クエリ用ユースケースを提供"""
    return OrderQueryInteractor(order_repo, presenter, error_presenter)
