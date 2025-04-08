# ドメイン駆動設計 (DDD) サンプルアプリケーション

このプロジェクトは、ドメイン駆動設計 (DDD) の概念とパターンを実践的に学ぶためのサンプルアプリケーションです。

## アーキテクチャ

このアプリケーションは、クリーンアーキテクチャとDDDの戦術的設計パターンを組み合わせて実装されています。

### ディレクトリ構造

```
app/
├── domain/               # ドメイン層
│   ├── entities/         # エンティティ
│   ├── aggregates/       # 集約
│   ├── services/         # ドメインサービス
│   ├── events/           # ドメインイベント
│   └── repositories/     # リポジトリインターフェース
│
├── usecases/             # アプリケーション層
│   
├── adapters/             # インフラストラクチャ/アダプタ層
│   ├── controllers/      # コントローラー
│   └── repositories/     # リポジトリ実装
│
├── dependencies.py       # 依存関係の注入設定
└── main.py               # アプリケーションのエントリーポイント
```

## 実装されたDDDパターン

1. **エンティティ**: 一意の識別子を持ち、時間とともに状態が変わるドメインオブジェクト (例: `Order`)
2. **値オブジェクト**: 不変で、属性の値によってのみ定義される概念 (例: `Address`)
3. **集約**: 一貫性の境界を定義し、関連するエンティティと値オブジェクトをカプセル化 (例: `OrderAggregate`)
4. **リポジトリ**: ドメインオブジェクトの永続化を抽象化 (例: `OrderRepository`)
5. **ドメインサービス**: 単一のエンティティに自然に属さないドメインロジック (例: `InventoryService`)
6. **ドメインイベント**: ドメイン内で発生した重要な出来事 (例: `OrderShippedEvent`)

## 使用方法

### 環境構築

```bash
pip install -r requirements.txt
```

### アプリケーション起動

```bash
python -m app.main
```

## APIエンドポイント

- `POST /orders` - 新しい注文を作成する

## 参考資料

- エリック・エヴァンスの「ドメイン駆動設計」
- ヴォーン・ヴァーノンの「実践ドメイン駆動設計」 