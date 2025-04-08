from domain.repositories.order_repository import (
    OrderCommandRepositoryInterface,
    OrderQueryRepositoryInterface
)
from config.environment import env
from infrastructure.repositories.in_memory_order_repository import (
    InMemoryOrderCommandRepository,
    InMemoryOrderQueryRepository
)

# 共有データストアを作成（本来はCQRSではコマンドとクエリで別々のデータストアを使用することが多い）
_order_store = {}

def get_order_command_repository(db_url: str | None = None) -> OrderCommandRepositoryInterface:
    """注文コマンドリポジトリのインスタンスを取得する

    Args:
        db_url (str | None, optional): データベースURL. Defaults to None.

    Returns:
        OrderCommandRepositoryInterface: コマンドリポジトリのインスタンス
    """
    if db_url is None:
        db_url = env.DATABASE_URL

    # コマンド用のデータストア（書き込み操作用）
    # 実際のプロダクションでは、書き込み用に最適化されたDBを使用する
    print(f"Connecting to Command database at {db_url}")
    repo = InMemoryOrderCommandRepository()
    repo.orders = _order_store
    return repo


def get_order_query_repository(db_url: str | None = None) -> OrderQueryRepositoryInterface:
    """注文クエリリポジトリのインスタンスを取得する

    Args:
        db_url (str | None, optional): データベースURL. Defaults to None.

    Returns:
        OrderQueryRepositoryInterface: クエリリポジトリのインスタンス
    """
    if db_url is None:
        db_url = env.DATABASE_URL

    # クエリ用のデータストア（読み取り操作用）
    # 実際のプロダクションでは、読み取り用に最適化されたDBを使用する
    print(f"Connecting to Query database at {db_url}")
    repo = InMemoryOrderQueryRepository()
    repo.orders = _order_store
    return repo