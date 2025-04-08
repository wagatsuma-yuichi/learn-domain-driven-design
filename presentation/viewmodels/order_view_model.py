from typing import Dict, List, Any, Optional
from fastapi import status

class OrderViewModel:
    """注文ビューモデル"""
    
    def __init__(self):
        self.order: Optional[Dict[str, Any]] = None
        self.orders: List[Dict[str, Any]] = []
        self.error: Optional[str] = None
        self.success: bool = False
    
    def set_order(self, order: Dict[str, Any]) -> None:
        """注文を設定する"""
        self.order = order
        self.success = True
        self.error = None
    
    def set_orders(self, orders: List[Dict[str, Any]]) -> None:
        """注文リストを設定する"""
        self.orders = orders
        self.success = True
        self.error = None
    
    def set_error(self, message: str) -> None:
        """エラーを設定する"""
        self.error = message
        self.success = False
    
    def to_dict(self) -> Dict[str, Any]:
        """ビューモデルをAPIレスポンス用の辞書に変換する"""
        result = {
            "success": self.success
        }
        
        if self.order:
            result["data"] = self.order
        elif self.orders:
            result["data"] = self.orders
        
        if self.error:
            result["error"] = self.error
            
        return result 
    

class HttpResponseOrderCreationViewModel(OrderViewModel):
    """注文情報を含むHTTP応答用ビューモデル"""
    
    def __init__(self, status_code: int = status.HTTP_201_CREATED):
        super().__init__()
        self.status_code = status_code
    
    def set_body(self, body: Dict[str, Any]) -> None:
        """ボディを設定する"""
        self.body = body
        

class HttpResponseOrderQueryViewModel(OrderViewModel):
    """注文情報を含むHTTP応答用ビューモデル"""
    
    def __init__(self, status_code: int = status.HTTP_200_OK):
        super().__init__()
        self.status_code = status_code

class HttpResponseOrderManagementViewModel(OrderViewModel):
    """注文情報を含むHTTP応答用ビューモデル"""
    
    def __init__(self, status_code: int = status.HTTP_200_OK):
        super().__init__()
        self.status_code = status_code


class HttpResponseOrderErrorViewModel(OrderViewModel):
    """注文情報を含むHTTP応答用ビューモデル"""
    
    def __init__(self, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__()
        self.status_code = status_code
