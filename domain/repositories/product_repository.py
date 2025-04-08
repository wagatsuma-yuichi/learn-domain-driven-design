from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from domain.entities.product import Product


class ProductRepository(ABC):
    """製品リポジトリのインターフェース"""
    
    @abstractmethod
    def save(self, product: Product) -> Product:
        """製品を保存する"""
        pass
    
    @abstractmethod
    def find_by_id(self, product_id: UUID) -> Optional[Product]:
        """IDで製品を検索する"""
        pass
    
    @abstractmethod
    def find_by_name(self, name: str) -> List[Product]:
        """名前で製品を検索する"""
        pass
    
    @abstractmethod
    def find_all(self) -> List[Product]:
        """全ての製品を取得する"""
        pass
    
    @abstractmethod
    def update(self, product: Product) -> Product:
        """製品を更新する"""
        pass
    
    @abstractmethod
    def delete(self, product_id: UUID) -> None:
        """製品を削除する"""
        pass 