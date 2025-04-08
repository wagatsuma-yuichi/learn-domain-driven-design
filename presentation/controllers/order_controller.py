from typing import Dict, Any, List, Optional
from uuid import UUID
from typing import Annotated
from application.interfaces.dto import OrderDTO, OrderItemDTO
from application.interfaces.order_use_case import (
    OrderCommandInputBoundary,
    OrderQueryInputBoundary,
)
from presentation.presenters.order_presenter import (
    OrderCommandPresenter,
    OrderQueryPresenter
)
from application.usecases.dependancies import (
    order_command_usecase,
    order_query_usecase
)
from fastapi import APIRouter, Depends
from pydantic import BaseModel

OrderRouter = APIRouter(prefix="/orders", tags=["orders"])

# Pydanticモデル
class OrderItemRequest(BaseModel):
    product_id: str
    quantity: int
    price_per_unit: float

class OrderRequest(BaseModel):
    customer_id: str
    items: List[OrderItemRequest]

class OrderStatusUpdate(BaseModel):
    status: str

class OrderItemResponse(BaseModel):
    product_id: str
    quantity: int
    price_per_unit: float
    total_price: float

class OrderResponse(BaseModel):
    order_id: Optional[str] = None
    customer_id: Optional[str] = None
    items: Optional[List[OrderItemResponse]] = None
    total_amount: Optional[float] = None
    status: Optional[str] = None
    created_at: Optional[str] = None
    error: Optional[str] = None

# コマンド（書き込み操作）
@OrderRouter.post("/", response_model=OrderResponse)
def create_order(
    request_data: OrderRequest,
    order_use_case: Annotated[OrderCommandInputBoundary, Depends(order_command_usecase)],
    presenter: OrderCommandPresenter = Depends()
) -> Dict[str, Any]:
    """注文を作成する"""
    try:
        # リクエストデータからDTOを作成
        order_dto = _create_order_dto_from_request(request_data.dict())
        
        # ユースケースを実行
        order_use_case.create_order(order_dto)
        
        # レスポンスを返す
        return presenter.view_model.to_dict()
        
    except ValueError as e:
        # UUIDの形式が不正な場合など
        presenter.present_error(f"Invalid input data: {str(e)}")
        return presenter.view_model.to_dict()
    except Exception as e:
        # その他のエラー
        presenter.present_error(f"Error in controller: {str(e)}")
        return presenter.view_model.to_dict()

@OrderRouter.put("/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: str,
    status_update: OrderStatusUpdate,
    order_use_case: Annotated[OrderCommandInputBoundary, Depends(order_command_usecase)],
    presenter: OrderCommandPresenter = Depends()
) -> Dict[str, Any]:
    """注文ステータスを更新する"""
    try:
        # 注文IDをUUIDに変換
        order_uuid = UUID(order_id)
        
        # ユースケースを実行
        order_use_case.update_order_status(order_uuid, status_update.status)
        
        # レスポンスを返す
        return presenter.view_model.to_dict()
        
    except ValueError as e:
        # UUIDの形式が不正な場合
        presenter.present_error(f"Invalid order ID format: {str(e)}")
        return presenter.view_model.to_dict()
    except Exception as e:
        # その他のエラー
        presenter.present_error(f"Error in controller: {str(e)}")
        return presenter.view_model.to_dict()

@OrderRouter.delete("/{order_id}", response_model=OrderResponse)
def cancel_order(
    order_id: str,
    order_use_case: Annotated[OrderCommandInputBoundary, Depends(order_command_usecase)],
    presenter: OrderCommandPresenter = Depends()
) -> Dict[str, Any]:
    """注文をキャンセルする"""
    try:
        # 注文IDをUUIDに変換
        order_uuid = UUID(order_id)
        
        # ユースケースを実行
        order_use_case.cancel_order(order_uuid)
        
        # レスポンスを返す
        return presenter.view_model.to_dict()
        
    except ValueError as e:
        # UUIDの形式が不正な場合
        presenter.present_error(f"Invalid order ID format: {str(e)}")
        return presenter.view_model.to_dict()
    except Exception as e:
        # その他のエラー
        presenter.present_error(f"Error in controller: {str(e)}")
        return presenter.view_model.to_dict()

# クエリ（読み取り操作）
@OrderRouter.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: str,
    order_use_case: Annotated[OrderQueryInputBoundary, Depends(order_query_usecase)],
    presenter: OrderQueryPresenter = Depends()
) -> Dict[str, Any]:
    """注文を取得する"""
    try:
        # 注文IDをUUIDに変換
        order_uuid = UUID(order_id)
        
        # ユースケースを実行
        order_use_case.get_order(order_uuid)
        
        # レスポンスを返す
        return presenter.view_model.to_dict()
        
    except ValueError as e:
        # UUIDの形式が不正な場合
        presenter.present_error(f"Invalid order ID format: {str(e)}")
        return presenter.view_model.to_dict()
    except Exception as e:
        # その他のエラー
        presenter.present_error(f"Error in controller: {str(e)}")
        return presenter.view_model.to_dict()

@OrderRouter.get("/customer/{customer_id}", response_model=OrderResponse)
def get_customer_orders(
    customer_id: str,
    order_use_case: Annotated[OrderQueryInputBoundary, Depends(order_query_usecase)],
    presenter: OrderQueryPresenter = Depends()
) -> Dict[str, Any]:
    """顧客の注文を取得する"""
    try:
        # 顧客IDをUUIDに変換
        customer_uuid = UUID(customer_id)
        
        # ユースケースを実行
        order_use_case.get_customer_orders(customer_uuid)
        
        # レスポンスを返す
        return presenter.view_model.to_dict()
        
    except ValueError as e:
        # UUIDの形式が不正な場合
        presenter.present_error(f"Invalid customer ID format: {str(e)}")
        return presenter.view_model.to_dict()
    except Exception as e:
        # その他のエラー
        presenter.present_error(f"Error in controller: {str(e)}")
        return presenter.view_model.to_dict()

def _create_order_dto_from_request(request_data: Dict[str, Any]) -> OrderDTO:
    """リクエストデータからOrderDTOを作成する"""
    try:
        # 顧客IDをUUIDに変換
        customer_id = UUID(request_data.get("customer_id", ""))
        
        # 注文アイテムを作成
        items = []
        for item_data in request_data.get("items", []):
            try:
                product_id = UUID(item_data.get("product_id", ""))
                item = OrderItemDTO(
                    product_id=product_id,
                    quantity=int(item_data.get("quantity", 0)),
                    price_per_unit=float(item_data.get("price_per_unit", 0.0) or 0.0)
                )
                items.append(item)
            except ValueError as e:
                # 個別の商品IDのエラーを詳細に報告
                raise ValueError(f"Invalid product ID: {item_data.get('product_id', '')}: {str(e)}")
        
        # 注文DTOを作成
        return OrderDTO(
            customer_id=customer_id,
            items=items
        )
    except ValueError as e:
        # UUID変換エラーなどを詳細に報告
        raise ValueError(f"Error creating Order DTO: {str(e)}")
    except Exception as e:
        # その他のエラー
        raise ValueError(f"Unexpected error in Order DTO creation: {str(e)}")

