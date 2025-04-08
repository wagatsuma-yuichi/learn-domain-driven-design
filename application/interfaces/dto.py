from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from uuid import UUID


@dataclass
class OrderItemDTO:
    """注文アイテムのデータ転送オブジェクト"""
    product_id: UUID
    quantity: int
    price_per_unit: float


@dataclass
class OrderDTO:
    """注文のデータ転送オブジェクト"""
    id: Optional[UUID] = None
    customer_id: UUID = None
    items: List[OrderItemDTO] = field(default_factory=list)
    status: str = "PENDING"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    total_amount: Optional[float] = None


@dataclass
class CustomerDTO:
    """顧客のデータ転送オブジェクト"""
    id: Optional[UUID] = None
    name: str = ""
    email: str = ""
    phone: Optional[str] = None
    address: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class ProductDTO:
    """製品のデータ転送オブジェクト"""
    id: Optional[UUID] = None
    name: str = ""
    description: Optional[str] = None
    price: float = 0.0
    stock_quantity: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None 