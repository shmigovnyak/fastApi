from fastapi import FastAPI
from routes.users_route import router as users_router
from routes.books_route import router as books_router
from service.db import engine, Base

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Включение роутера пользователей
app.include_router(users_router)

# Включение роутера книг
app.include_router(books_router)



