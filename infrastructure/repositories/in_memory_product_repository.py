from typing import Dict, List, Optional
from uuid import UUID

from domain.entities.product import Product
from domain.repositories.product_repository import ProductRepository


class InMemoryProductRepository(ProductRepository):
    """メモリ内製品リポジトリの実装"""
    
    def __init__(self):
        self.products: Dict[UUID, Product] = {}
    
    def save(self, product: Product) -> Product:
        """製品を保存する"""
        self.products[product.id] = product
        return product
    
    def find_by_id(self, product_id: UUID) -> Optional[Product]:
        """IDで製品を検索する"""
        return self.products.get(product_id)
    
    def find_by_name(self, name: str) -> List[Product]:
        """名前で製品を検索する"""
        return [product for product in self.products.values() if name.lower() in product.name.lower()]
    
    def find_all(self) -> List[Product]:
        """全ての製品を取得する"""
        return list(self.products.values())
    
    def update(self, product: Product) -> Product:
        """製品を更新する"""
        if product.id in self.products:
            self.products[product.id] = product
        return product
    
    def delete(self, product_id: UUID) -> None:
        """製品を削除する"""
        if product_id in self.products:
            del self.products[product_id] 