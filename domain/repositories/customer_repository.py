from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from domain.entities.customer import Customer


class CustomerRepository(ABC):
    """顧客リポジトリのインターフェース"""
    
    @abstractmethod
    def save(self, customer: Customer) -> Customer:
        """顧客を保存する"""
        pass
    
    @abstractmethod
    def find_by_id(self, customer_id: UUID) -> Optional[Customer]:
        """IDで顧客を検索する"""
        pass
    
    @abstractmethod
    def find_by_email(self, email: str) -> Optional[Customer]:
        """メールアドレスで顧客を検索する"""
        pass
    
    @abstractmethod
    def find_all(self) -> List[Customer]:
        """全ての顧客を取得する"""
        pass
    
    @abstractmethod
    def update(self, customer: Customer) -> Customer:
        """顧客を更新する"""
        pass
    
    @abstractmethod
    def delete(self, customer_id: UUID) -> None:
        """顧客を削除する"""
        pass 