from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

# Модель пользователя
class User(BaseModel):
    id: Optional[int] = None # ID будет генерироваться сервером при создании
    username: str
    email: str

# Модель для создания пользователя (без ID)
class UserCreate(BaseModel):
    username: str
    email: str

# Хранилище пользователей в памяти (для примера)
users_list: List[User] = []
user_id_counter = 0

router = APIRouter(
    prefix="/v1/users",
    tags=["users"],
)

@router.post("/", response_model=User)
async def create_user(user: UserCreate):
    global user_id_counter
    user_id_counter += 1
    new_user = User(id=user_id_counter, username=user.username, email=user.email)
    users_list.append(new_user)
    return new_user

@router.get("/", response_model=List[User])
async def read_users():
    return users_list

@router.get("/{user_id}", response_model=User)
async def read_user(user_id: int):
    for user in users_list:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, user_update: UserCreate):
    for i, user in enumerate(users_list):
        if user.id == user_id:
            updated_user = User(id=user_id, username=user_update.username, email=user_update.email)
            users_list[i] = updated_user
            return updated_user
    raise HTTPException(status_code=404, detail="User not found")

@router.delete("/{user_id}", response_model=dict)
async def delete_user(user_id: int):
    global users_list
    initial_len = len(users_list)
    users_list = [user for user in users_list if user.id != user_id]
    if len(users_list) < initial_len:
        return {"detail": "User deleted"}
    raise HTTPException(status_code=404, detail="User not found") 