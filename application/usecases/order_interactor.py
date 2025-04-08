from typing import List
from uuid import UUID

from application.interfaces.dto import OrderDTO, OrderItemDTO
from application.interfaces.order_use_case import (
    OrderCreationInputBoundary, OrderQueryInputBoundary, OrderManagementInputBoundary,
    OrderCreationOutputBoundary, OrderQueryOutputBoundary, OrderManagementOutputBoundary, OrderErrorOutputBoundary
)
from domain.entities.order import Order, OrderItem
from domain.repositories.order_repository import OrderRepositoryInterface
from domain.repositories.product_repository import ProductRepository
from domain.repositories.customer_repository import CustomerRepository


def _to_dto(order: Order) -> OrderDTO:
    """OrderエンティティをOrderDTOに変換する (共通ユーティリティ関数)"""
    item_dtos = [
        OrderItemDTO(
            product_id=item.product_id,
            quantity=item.quantity,
            price_per_unit=item.price_per_unit
        )
        for item in order.items
    ]
    
    return OrderDTO(
        id=order.id,
        customer_id=order.customer_id,
        items=item_dtos,
        status=order.status,
        created_at=order.created_at,
        updated_at=order.updated_at,
        total_amount=order.total_amount
    )


class OrderCreationInteractor(OrderCreationInputBoundary):
    """注文作成の責務を持つインタラクター"""
    
    def __init__(self, 
                order_repository: OrderRepositoryInterface,
                customer_repository: CustomerRepository,
                product_repository: ProductRepository, 
                output_boundary: OrderCreationOutputBoundary,
                error_boundary: OrderErrorOutputBoundary):
        self.order_repository = order_repository
        self.customer_repository = customer_repository
        self.product_repository = product_repository
        self.output_boundary = output_boundary
        self.error_boundary = error_boundary
    
    def create_order(self, order_dto: OrderDTO) -> OrderDTO:
        """注文を作成する"""
        try:
            # 顧客が存在するか確認
            customer = self.customer_repository.find_by_id(order_dto.customer_id)
            if not customer:
                self.error_boundary.present_error(f"Customer with ID {order_dto.customer_id} not found")
                return order_dto
            
            # 注文エンティティの作成
            order = Order(
                customer_id=order_dto.customer_id,
                status="PENDING"
            )
            
            # 注文アイテムの追加
            for item_dto in order_dto.items:
                # 製品が存在するか確認
                product = self.product_repository.find_by_id(item_dto.product_id)
                if not product:
                    self.error_boundary.present_error(f"Product with ID {item_dto.product_id} not found")
                    return order_dto
                
                # 在庫が十分にあるか確認
                if product.stock_quantity < item_dto.quantity:
                    self.error_boundary.present_error(
                        f"Not enough stock for product {product.name}. Available: {product.stock_quantity}, Requested: {item_dto.quantity}"
                    )
                    return order_dto
                
                # 注文アイテムの作成
                order_item = OrderItem(
                    product_id=item_dto.product_id,
                    quantity=item_dto.quantity,
                    price_per_unit=product.price
                )
                
                # 注文に追加
                order.add_item(order_item)
                
                # 在庫を更新
                product.update_stock(product.stock_quantity - item_dto.quantity)
                self.product_repository.update(product)
            
            # 注文を保存
            saved_order = self.order_repository.save(order)
            
            # DTOに変換して返す
            result_dto = _to_dto(saved_order)
            self.output_boundary.present_created_order(result_dto)
            return result_dto
            
        except Exception as e:
            self.error_boundary.present_error(f"Error creating order: {str(e)}")
            return order_dto


class OrderQueryInteractor(OrderQueryInputBoundary):
    """注文照会の責務を持つインタラクター"""
    
    def __init__(self, 
                order_repository: OrderRepositoryInterface,
                output_boundary: OrderQueryOutputBoundary,
                error_boundary: OrderErrorOutputBoundary):
        self.order_repository = order_repository
        self.output_boundary = output_boundary
        self.error_boundary = error_boundary
    
    def get_order(self, order_id: UUID) -> OrderDTO:
        """注文を取得する"""
        try:
            order = self.order_repository.find_by_id(order_id)
            if not order:
                self.error_boundary.present_error(f"Order with ID {order_id} not found")
                return OrderDTO()
            
            order_dto = _to_dto(order)
            self.output_boundary.present_order(order_dto)
            return order_dto
            
        except Exception as e:
            self.error_boundary.present_error(f"Error getting order: {str(e)}")
            return OrderDTO()
    
    def get_customer_orders(self, customer_id: UUID) -> List[OrderDTO]:
        """顧客の注文を取得する"""
        try:
            orders = self.order_repository.find_all_by_customer_id(customer_id)
            order_dtos = [_to_dto(order) for order in orders]
            self.output_boundary.present_orders(order_dtos)
            return order_dtos
            
        except Exception as e:
            self.error_boundary.present_error(f"Error getting customer orders: {str(e)}")
            return []


class OrderManagementInteractor(OrderManagementInputBoundary):
    """注文管理の責務を持つインタラクター"""
    
    def __init__(self, 
                order_repository: OrderRepositoryInterface,
                product_repository: ProductRepository,
                output_boundary: OrderManagementOutputBoundary,
                error_boundary: OrderErrorOutputBoundary):
        self.order_repository = order_repository
        self.product_repository = product_repository
        self.output_boundary = output_boundary
        self.error_boundary = error_boundary
    
    def update_order_status(self, order_id: UUID, status: str) -> OrderDTO:
        """注文ステータスを更新する"""
        try:
            order = self.order_repository.find_by_id(order_id)
            if not order:
                self.error_boundary.present_error(f"Order with ID {order_id} not found")
                return OrderDTO()
            
            order.update_status(status)
            updated_order = self.order_repository.update(order)
            
            order_dto = _to_dto(updated_order)
            self.output_boundary.present_updated_order(order_dto)
            return order_dto
            
        except Exception as e:
            self.error_boundary.present_error(f"Error updating order status: {str(e)}")
            return OrderDTO()
    
    def cancel_order(self, order_id: UUID) -> OrderDTO:
        """注文をキャンセルする"""
        try:
            order = self.order_repository.find_by_id(order_id)
            if not order:
                self.error_boundary.present_error(f"Order with ID {order_id} not found")
                return OrderDTO()
            
            # キャンセルできるのはPENDINGまたはCONFIRMEDの注文のみ
            if order.status not in ["PENDING", "CONFIRMED"]:
                self.error_boundary.present_error(f"Cannot cancel order with status {order.status}")
                return _to_dto(order)
            
            # 注文ステータスを更新
            order.update_status("CANCELLED")
            
            # 在庫を戻す
            for item in order.items:
                product = self.product_repository.find_by_id(item.product_id)
                if product:
                    product.update_stock(product.stock_quantity + item.quantity)
                    self.product_repository.update(product)
            
            # 更新した注文を保存
            updated_order = self.order_repository.update(order)
            
            order_dto = _to_dto(updated_order)
            self.output_boundary.present_cancelled_order(order_dto)
            return order_dto
            
        except Exception as e:
            self.error_boundary.present_error(f"Error cancelling order: {str(e)}")
            return OrderDTO() 