from typing import List
from fastapi import HTTPException
from schemas.user_schemas import User, UserCreate

users_list: List[User] = []
user_id_counter = 0

async def create_user(user: UserCreate) -> User:
    global user_id_counter
    user_id_counter += 1
    new_user = User(id=user_id_counter, username=user.username, email=user.email, is_active=True)
    users_list.append(new_user)
    return new_user

async def read_users() -> List[User]:
    return users_list

async def read_user(user_id: int) -> User:
    for user in users_list:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

async def update_user(user_id: int, user_update: UserCreate) -> User:
    for i, user in enumerate(users_list):
        if user.id == user_id:
            updated_user = User(id=user_id, username=user_update.username, email=user_update.email, is_active=user.is_active)
            users_list[i] = updated_user
            return updated_user
    raise HTTPException(status_code=404, detail="User not found")

async def delete_user(user_id: int) -> dict:
    global users_list
    initial_len = len(users_list)
    users_list = [user for user in users_list if user.id != user_id]
    if len(users_list) < initial_len:
        return {"detail": "User deleted"}
    raise HTTPException(status_code=404, detail="User not found") 