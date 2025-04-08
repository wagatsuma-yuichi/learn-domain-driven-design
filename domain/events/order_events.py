from dataclasses import dataclass
from datetime import datetime

@dataclass
class OrderShippedEvent:
    order_id: str
    shipped_at: datetime
    tracking_number: str

@dataclass
class OrderItemAddedEvent:
    product_id: str
    quantity: int 