from functools import lru_cache
import os

from pydantic_settings import BaseSettings


@lru_cache
def get_env_filename():
    runtime_env = os.getenv("APP_ENV")
    return f".env.{runtime_env}.local" if runtime_env else ".env"


class EnvironmentSettings(BaseSettings):
    API_VERSION: str = os.getenv("API_VERSION", "v1")
    APP_NAME: str = os.getenv("APP_NAME", "Clean Architecture DI Demo")
    APP_ENV: str = os.getenv("APP_ENV", "development")
    DATABASE_DIALECT: str = os.getenv("DATABASE_DIALECT", "sqlite")
    DATABASE_HOSTNAME: str = os.getenv("DATABASE_HOSTNAME", "localhost")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", ":memory:")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "")
    DATABASE_PORT: int = os.getenv("DATABASE_PORT", 5432)
    DATABASE_USERNAME: str = os.getenv("DATABASE_USERNAME", "")
    DEBUG_MODE: bool = os.getenv("DEBUG_MODE", "true").lower() == "true"

    # データベースURL（計算プロパティ）
    @property
    def DATABASE_URL(self) -> str:
        if self.USE_MOCK_DB:
            return None
        if not all([
            self.DATABASE_DIALECT,
            self.DATABASE_USERNAME,
            self.DATABASE_PASSWORD,
            self.DATABASE_HOSTNAME,
            self.DATABASE_PORT,
            self.DATABASE_NAME
        ]):
            return None
        # PostgreSQLのURL形式のみをサポート
        return f"postgresql://{self.DATABASE_USERNAME}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOSTNAME}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
    
    # 環境に応じてモックDBを使用するかどうかを決定
    @property
    def USE_MOCK_DB(self) -> bool:
        return self.APP_ENV.lower() in ["development", "develop", "test"]

    model_config = {
        "env_file": get_env_filename(),
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
        "env_prefix": "",
        "extra": "allow"
    }


@lru_cache
def get_environment_variables():
    return EnvironmentSettings()


# シングルトンとしてのインスタンス
env = get_environment_variables() 