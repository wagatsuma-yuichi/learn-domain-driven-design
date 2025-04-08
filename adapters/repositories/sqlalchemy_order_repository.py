from domain.repositories.order_repository import OrderRepository
from domain.aggregates.order_aggregate import OrderAggregate
from domain.entities.order import Order, OrderItem

class SQLAlchemyOrderRepository(OrderRepository):
    def __init__(self, session):
        self.session = session

    def find_by_id(self, order_id: str) -> OrderAggregate:
        # データベースから集約全体を復元
        order = self.session.query(Order).get(order_id)
        if not order:
            return None
            
        items = self.session.query(OrderItem).filter(OrderItem.order_id == order_id).all()
        return OrderAggregate(order, items)

    def save(self, order_aggregate: OrderAggregate) -> None:
        # 集約全体を永続化
        self.session.add(order_aggregate.order)
        for item in order_aggregate.items:
            self.session.add(item)
        self.session.commit() 