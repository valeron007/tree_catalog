import uvicorn
from fastapi import FastAPI

from src.routes.order.routes import order_router

app = FastAPI()

app.include_router(order_router, prefix='/order')

if __name__ == "__main__":
    uvicorn.run('main:app', host='127.0.0.1', port=8001, reload=True)
