from domain.repositories.order_repository import OrderRepositoryInterface
from config.environment import env
from infrastructure.repositories.in_memory_order_repository import InMemoryOrderRepository

def get_order_repository(db_url: str | None = None) -> OrderRepositoryInterface:
    """リポジトリのインスタンスを取得する

    Args:
        db_url (str | None, optional): データベースURL. Defaults to None.

    Returns:
        UserRepository: リポジトリのインスタンス
    """
    if db_url is None:
        db_url = env.DATABASE_URL

    # PostgreSQLに接続
    print(f"Connecting to PostgreSQL database at {db_url}")
    return InMemoryOrderRepository()