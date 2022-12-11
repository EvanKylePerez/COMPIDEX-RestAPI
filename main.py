from fastapi import FastAPI
from routes.todo_routes import user_api_router, merchant_api_router, product_api_router

app = FastAPI()

# App routers
app.include_router(user_api_router)
app.include_router(merchant_api_router)
app.include_router(product_api_router)
