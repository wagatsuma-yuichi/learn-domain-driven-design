from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class Product:
    """製品エンティティ"""
    name: str
    price: float
    id: UUID = field(default_factory=uuid4)
    description: Optional[str] = None
    stock_quantity: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    
    def update_stock(self, quantity: int) -> None:
        """在庫数を更新する"""
        self.stock_quantity = quantity
        self.updated_at = datetime.now()
        
    def update_price(self, price: float) -> None:
        """価格を更新する"""
        self.price = price
        self.updated_at = datetime.now()
        
    def is_available(self) -> bool:
        """製品が利用可能かどうか確認する"""
        return self.stock_quantity > 0 