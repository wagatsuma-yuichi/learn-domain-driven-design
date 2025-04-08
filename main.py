from fastapi import FastAPI, Depends, HTTPException
from typing import List, Dict, Any
import uvicorn
from pydantic import BaseModel

from dependencies import get_order_controller
from adapters.controllers.order_controller import OrderController

app = FastAPI(title="ドメイン駆動設計サンプルアプリ")

class OrderItemModel(BaseModel):
    product_id: str
    quantity: int

class CreateOrderRequest(BaseModel):
    customer_id: str
    items: List[OrderItemModel]

@app.post("/orders", response_model=Dict[str, Any])
async def create_order(
    request: CreateOrderRequest,
    order_controller: OrderController = Depends(get_order_controller)
):
    """注文を作成するエンドポイント"""
    try:
        items = [{"product_id": item.product_id, "quantity": item.quantity} for item in request.items]
        return order_controller.create_order(request.customer_id, items)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
