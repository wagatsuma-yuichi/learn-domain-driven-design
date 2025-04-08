from pydantic import BaseModel
from typing import List, Optional


# Pydanticモデルの定義
class CustomerResponse(BaseModel):
    id: str
    name: str
    email: str

class ProductResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    price: float
    stock_quantity: int

class SampleDataResponse(BaseModel):
    customers: List[CustomerResponse]
    products: List[ProductResponse]

class OrderItemRequest(BaseModel):
    product_id: str
    quantity: int
    price_per_unit: Optional[float] = None

class OrderRequest(BaseModel):
    customer_id: str
    items: List[OrderItemRequest]

class OrderStatusRequest(BaseModel):
    status: str
