import uvicorn
from fastapi import FastAPI

from config.environment import env
from presentation.controllers.order_controller import OrderRouter
from fastapi.middleware.cors import CORSMiddleware

# アプリケーション作成
app = FastAPI(title=env.APP_NAME)

# CORSミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # development環境以外ではallow_credentialsをTrueに設定
    allow_credentials=True if env.APP_ENV != "development" else False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# APIルートを登録
app.include_router(OrderRouter, prefix="/api")

@app.get("/", tags=["root"])
async def root():
    return {
        "message": f"{env.APP_NAME} API",
        "version": env.API_VERSION,
        "environment": env.APP_ENV,
        "using_mock": env.USE_MOCK_DB,
        "database_url": env.DATABASE_URL
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=env.DEBUG_MODE)