from fastapi import FastAPI
from routes.users_route import router as users_router
from routes.books_route import router as books_router

app = FastAPI()

# Включение роутера пользователей
app.include_router(users_router)

# Включение роутера книг
app.include_router(books_router)


@app.get("/")
async def home():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
