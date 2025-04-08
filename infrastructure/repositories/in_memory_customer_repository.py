from typing import Dict, List, Optional
from uuid import UUID

from domain.entities.customer import Customer
from domain.repositories.customer_repository import CustomerRepository


class InMemoryCustomerRepository(CustomerRepository):
    """メモリ内顧客リポジトリの実装"""
    
    def __init__(self):
        self.customers: Dict[UUID, Customer] = {}
    
    def save(self, customer: Customer) -> Customer:
        """顧客を保存する"""
        self.customers[customer.id] = customer
        return customer
    
    def find_by_id(self, customer_id: UUID) -> Optional[Customer]:
        """IDで顧客を検索する"""
        return self.customers.get(customer_id)
    
    def find_by_email(self, email: str) -> Optional[Customer]:
        """メールアドレスで顧客を検索する"""
        for customer in self.customers.values():
            if customer.email == email:
                return customer
        return None
    
    def find_all(self) -> List[Customer]:
        """全ての顧客を取得する"""
        return list(self.customers.values())
    
    def update(self, customer: Customer) -> Customer:
        """顧客を更新する"""
        if customer.id in self.customers:
            self.customers[customer.id] = customer
        return customer
    
    def delete(self, customer_id: UUID) -> None:
        """顧客を削除する"""
        if customer_id in self.customers:
            del self.customers[customer_id] 