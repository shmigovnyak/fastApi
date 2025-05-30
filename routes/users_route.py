from fastapi import APIRouter, HTTPException
from typing import List, Optional
from schemas.user_schemas import User, UserCreate
from service import user_service

router = APIRouter(
    prefix="/v1/users",
    tags=["users"],
)

@router.post("/", response_model=User)
async def create_user_route(user: UserCreate):
    return await user_service.create_user(user)

@router.get("/", response_model=List[User])
async def read_users_route():
    return await user_service.read_users()

@router.get("/{user_id}", response_model=User)
async def read_user_route(user_id: int):
    return await user_service.read_user(user_id)

@router.put("/{user_id}", response_model=User)
async def update_user_route(user_id: int, user_update: UserCreate):
    return await user_service.update_user(user_id, user_update)

@router.delete("/{user_id}", response_model=dict)
async def delete_user_route(user_id: int):
    return await user_service.delete_user(user_id) 