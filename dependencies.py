from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from domain.services.inventory_service import InventoryService
from domain.repositories.order_repository import OrderRepository
from adapters.repositories.sqlalchemy_order_repository import SQLAlchemyOrderRepository
from usecases.create_order import CreateOrderUseCase
from adapters.controllers.order_controller import OrderController

# データベース設定
DATABASE_URL = "sqlite:///./app.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session() -> Session:
    """データベースセッションを取得する"""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def get_order_repository(session: Session = None) -> OrderRepository:
    """注文リポジトリを取得する"""
    if session is None:
        session = next(get_db_session())
    return SQLAlchemyOrderRepository(session)

def get_inventory_service() -> InventoryService:
    """在庫サービスを取得する"""
    # 実際の実装ではリポジトリが必要
    return InventoryService(None)  # 仮のNoneを渡しています

def get_create_order_use_case() -> CreateOrderUseCase:
    """注文作成ユースケースを取得する"""
    return CreateOrderUseCase(
        order_repository=get_order_repository(),
        inventory_service=get_inventory_service()
    )

def get_order_controller() -> OrderController:
    """注文コントローラーを取得する"""
    return OrderController(get_create_order_use_case())
