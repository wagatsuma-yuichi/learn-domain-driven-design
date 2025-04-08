from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class Customer:
    """顧客エンティティ"""
    name: str
    email: str
    id: UUID = field(default_factory=uuid4)
    phone: Optional[str] = None
    address: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    
    def update_details(self, name: Optional[str] = None, email: Optional[str] = None, 
                      phone: Optional[str] = None, address: Optional[str] = None) -> None:
        """顧客の詳細を更新する"""
        if name:
            self.name = name
        if email:
            self.email = email
        if phone is not None:  # None を設定可能にする
            self.phone = phone
        if address is not None:  # None を設定可能にする
            self.address = address
        self.updated_at = datetime.now() 