from fastapi import FastAPI
from routers import menu, orders

app = FastAPI(title="Restaurant Ordering System")

app.include_router(menu.router, prefix="/menu", tags=["Menu"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])
