import unittest
from uuid import UUID, uuid4
from datetime import datetime

from domain.entities.order import Order, OrderItem
from domain.entities.customer import Customer
from domain.entities.product import Product
from application.interfaces.dto import OrderDTO, OrderItemDTO
from application.usecases.order_interactor import OrderCreationInteractor
from infrastructure.repositories.in_memory_order_repository import InMemoryOrderRepository
from infrastructure.repositories.in_memory_customer_repository import InMemoryCustomerRepository
from infrastructure.repositories.in_memory_product_repository import InMemoryProductRepository
from presentation.presenters.order_presenter import OrderCreationPresenter


class TestOrderCreation(unittest.TestCase):
    """注文作成機能のテストケース"""

    def setUp(self):
        """テスト前の準備"""
        # リポジトリの初期化
        self.order_repository = InMemoryOrderRepository()
        self.customer_repository = InMemoryCustomerRepository()
        self.product_repository = InMemoryProductRepository()

        # プレゼンターの初期化
        self.presenter = OrderCreationPresenter()

        # インタラクターの初期化
        self.interactor = OrderCreationInteractor(
            order_repository=self.order_repository,
            customer_repository=self.customer_repository,
            product_repository=self.product_repository,
            output_boundary=self.presenter,
            error_boundary=self.presenter
        )

        # テスト用データの準備
        self.customer = Customer(
            name="テスト顧客",
            email="test@example.com"
        )
        self.customer_repository.save(self.customer)

        self.product1 = Product(
            name="テスト商品1",
            price=1000,
            stock_quantity=10
        )
        self.product_repository.save(self.product1)

        self.product2 = Product(
            name="テスト商品2",
            price=2000,
            stock_quantity=5
        )
        self.product_repository.save(self.product2)

    def test_create_order_success(self):
        """注文作成の成功テスト"""
        # 注文DTOの準備
        order_dto = OrderDTO(
            customer_id=self.customer.id,
            items=[
                OrderItemDTO(
                    product_id=self.product1.id,
                    quantity=2,
                    price_per_unit=self.product1.price
                ),
                OrderItemDTO(
                    product_id=self.product2.id,
                    quantity=1,
                    price_per_unit=self.product2.price
                )
            ]
        )

        # 注文作成の実行
        result_dto = self.interactor.create_order(order_dto)

        # 検証
        self.assertIsNotNone(result_dto.id)
        self.assertEqual(result_dto.customer_id, self.customer.id)
        self.assertEqual(len(result_dto.items), 2)
        self.assertEqual(result_dto.status, "PENDING")
        self.assertIsNotNone(result_dto.created_at)
        
        # 合計金額のチェック
        expected_total = (self.product1.price * 2) + (self.product2.price * 1)
        self.assertEqual(result_dto.total_amount, expected_total)
        
        # リポジトリに保存されているかチェック
        saved_order = self.order_repository.find_by_id(result_dto.id)
        self.assertIsNotNone(saved_order)
        
        # 在庫が減少しているかチェック
        updated_product1 = self.product_repository.find_by_id(self.product1.id)
        self.assertEqual(updated_product1.stock_quantity, 8)  # 10 - 2
        
        updated_product2 = self.product_repository.find_by_id(self.product2.id)
        self.assertEqual(updated_product2.stock_quantity, 4)  # 5 - 1
        
        # プレゼンターにデータが設定されているかチェック
        self.assertIsNone(self.presenter.view_model.error)
        self.assertTrue(self.presenter.view_model.success)
        self.assertIsNotNone(self.presenter.view_model.order)

    def test_create_order_invalid_customer(self):
        """存在しない顧客IDによる注文作成失敗のテスト"""
        # 存在しない顧客IDの注文DTOを準備
        invalid_customer_id = uuid4()
        order_dto = OrderDTO(
            customer_id=invalid_customer_id,
            items=[
                OrderItemDTO(
                    product_id=self.product1.id,
                    quantity=1,
                    price_per_unit=self.product1.price
                )
            ]
        )

        # 注文作成の実行
        result_dto = self.interactor.create_order(order_dto)

        # エラーが発生し、注文が作成されていないことを検証
        self.assertIsNone(result_dto.id)
        self.assertFalse(self.presenter.view_model.success)
        self.assertIsNotNone(self.presenter.view_model.error)
        self.assertIn(f"Customer with ID {invalid_customer_id}", self.presenter.view_model.error)

    def test_create_order_invalid_product(self):
        """存在しない商品IDによる注文作成失敗のテスト"""
        # 存在しない商品IDの注文DTOを準備
        invalid_product_id = uuid4()
        order_dto = OrderDTO(
            customer_id=self.customer.id,
            items=[
                OrderItemDTO(
                    product_id=invalid_product_id,
                    quantity=1,
                    price_per_unit=1000
                )
            ]
        )

        # 注文作成の実行
        result_dto = self.interactor.create_order(order_dto)

        # エラーが発生し、注文が作成されていないことを検証
        self.assertIsNone(result_dto.id)
        self.assertFalse(self.presenter.view_model.success)
        self.assertIsNotNone(self.presenter.view_model.error)
        self.assertIn(f"Product with ID {invalid_product_id}", self.presenter.view_model.error)

    def test_create_order_insufficient_stock(self):
        """在庫不足による注文作成失敗のテスト"""
        # 在庫を超える数量の注文DTOを準備
        order_dto = OrderDTO(
            customer_id=self.customer.id,
            items=[
                OrderItemDTO(
                    product_id=self.product1.id,
                    quantity=20,  # 在庫は10のみ
                    price_per_unit=self.product1.price
                )
            ]
        )

        # 注文作成の実行
        result_dto = self.interactor.create_order(order_dto)

        # エラーが発生し、注文が作成されていないことを検証
        self.assertIsNone(result_dto.id)
        self.assertFalse(self.presenter.view_model.success)
        self.assertIsNotNone(self.presenter.view_model.error)
        self.assertIn("Not enough stock", self.presenter.view_model.error)
