from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4


@dataclass
class OrderItem:
    """注文アイテムエンティティ"""
    product_id: UUID
    quantity: int
    price_per_unit: float
    
    @property
    def total_price(self) -> float:
        return self.quantity * self.price_per_unit


@dataclass
class Order:
    """注文エンティティ"""
    id: UUID = field(default_factory=uuid4)
    customer_id: UUID = None
    items: List[OrderItem] = field(default_factory=list)
    status: str = "PENDING"  # PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    
    @property
    def total_amount(self) -> float:
        return sum(item.total_price for item in self.items)
    
    def add_item(self, item: OrderItem) -> None:
        self.items.append(item)
        self.updated_at = datetime.now()
        
    def remove_item(self, product_id: UUID) -> None:
        self.items = [item for item in self.items if item.product_id != product_id]
        self.updated_at = datetime.now()
        
    def update_status(self, status: str) -> None:
        self.status = status
        self.updated_at = datetime.now() 