from abc import ABC, abstractmethod
from domain.aggregates.order_aggregate import OrderAggregate

class OrderRepository(ABC):
    @abstractmethod
    def find_by_id(self, order_id: str) -> OrderAggregate:
        pass

    @abstractmethod
    def save(self, order: OrderAggregate) -> None:
        pass 