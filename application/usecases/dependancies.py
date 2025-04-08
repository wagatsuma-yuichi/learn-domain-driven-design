from fastapi import Depends
from typing import Annotated
from fastapi import status
from application.interfaces.order_use_case import (
    OrderCreationInputBoundary,
    OrderCreationOutputBoundary,
    OrderErrorOutputBoundary
)
from application.interfaces.dto import OrderDTO
from presentation.presenters.order_presenter import OrderCreationPresenter
from presentation.viewmodels.order_view_model import HttpResponseOrderCreationViewModel
from infrastructure.repositories.in_memory_order_repository import InMemoryOrderRepository
from config.database import get_order_repository
from application.usecases.order_interactor import OrderCreationInteractor
from domain.repositories.customer_repository import CustomerRepository
from domain.repositories.product_repository import ProductRepository
from infrastructure.repositories.in_memory_customer_repository import InMemoryCustomerRepository
from infrastructure.repositories.in_memory_product_repository import InMemoryProductRepository

def get_order_creation_presenter() -> OrderCreationOutputBoundary:
    """注文作成用プレゼンターを提供"""
    return HttpResponseOrderCreationPresenter()

def get_error_presenter() -> OrderErrorOutputBoundary:
    """エラー用プレゼンターを提供"""
    return HttpResponseOrderCreationPresenter()

def get_customer_repository() -> CustomerRepository:
    """顧客リポジトリを提供"""
    return InMemoryCustomerRepository()

def get_product_repository() -> ProductRepository:
    """製品リポジトリを提供"""
    return InMemoryProductRepository()

class HttpResponseOrderCreationPresenter(OrderCreationOutputBoundary, OrderErrorOutputBoundary):
    """注文作成結果をHTTPレスポンス用に変換するプレゼンター"""
    
    def __init__(self):
        self.view_model = HttpResponseOrderCreationViewModel()
    
    def present_created_order(self, order_dto: OrderDTO) -> None:
        """作成された注文を表示する"""
        self.view_model = HttpResponseOrderCreationViewModel(status.HTTP_201_CREATED)
        order_data = self._to_dict(order_dto)
        self.view_model.set_body(order_data)
        if order_dto.id:
            self.view_model.add_header("Location", f"/orders/{order_dto.id}")
    
    def output(self, output_data: OrderCreationOutputBoundary) -> None:
        """ユーザー登録結果をビューモデルに変換"""
        self.view_model = HttpResponseOrderCreationViewModel(status.HTTP_201_CREATED)
        self.view_model.set_body(output_data.to_dict())
        self.view_model.add_header("Location", f"/users/{output_data.id}")
    
    def output_error(self, output_data: OrderErrorOutputBoundary) -> None:
        """エラー情報をビューモデルに変換"""
        self.view_model = HttpResponseOrderCreationViewModel(output_data.status_code, output_data.message)
    
    def present_error(self, message: str) -> None:
        """エラーを表示する"""
        self.view_model = HttpResponseOrderCreationViewModel(status.HTTP_400_BAD_REQUEST)
        self.view_model.set_error(message)
    
    def get_view_model(self) -> HttpResponseOrderCreationViewModel:
        """ビューモデルを取得"""
        return self.view_model
    
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


def order_add_usecase(
    order_repo: Annotated[InMemoryOrderRepository, Depends(get_order_repository)],
    customer_repo: Annotated[CustomerRepository, Depends(get_customer_repository)],
    product_repo: Annotated[ProductRepository, Depends(get_product_repository)],
    presenter: Annotated[OrderCreationOutputBoundary, Depends(get_order_creation_presenter)],
    error_presenter: Annotated[OrderErrorOutputBoundary, Depends(get_error_presenter)]
) -> OrderCreationInputBoundary:
    """注文作成用ユースケースを提供"""
    return OrderCreationInteractor(order_repo, customer_repo, product_repo, presenter, error_presenter)