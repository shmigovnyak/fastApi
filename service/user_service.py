from typing import List
from fastapi import HTTPException
from schemas.user_schemas import User, UserCreate
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from service.db import SessionLocal
from service.models import User as UserModel

users_list: List[User] = []
user_id_counter = 0

async def create_user(user: UserCreate) -> User:
    async with SessionLocal() as session:
        db_user = UserModel(username=user.username, email=user.email)
        session.add(db_user)
        try:
            await session.commit()
            await session.refresh(db_user)
        except IntegrityError:
            await session.rollback()
            raise HTTPException(status_code=400, detail="Email already exists")
        return User.from_orm(db_user)

async def read_users() -> list[User]:
    async with SessionLocal() as session:
        result = await session.execute(select(UserModel).where(UserModel.is_active == True))
        users = result.scalars().all()
        return [User.from_orm(u) for u in users]

async def read_user(user_id: int) -> User:
    async with SessionLocal() as session:
        user = await session.get(UserModel, user_id)
        if not user or not user.is_active:
            raise HTTPException(status_code=404, detail="User not found")
        return User.from_orm(user)

async def update_user(user_id: int, user_update: UserCreate) -> User:
    async with SessionLocal() as session:
        user = await session.get(UserModel, user_id)
        if not user or not user.is_active:
            raise HTTPException(status_code=404, detail="User not found")
        user.username = user_update.username
        user.email = user_update.email
        try:
            await session.commit()
            await session.refresh(user)
        except IntegrityError:
            await session.rollback()
            raise HTTPException(status_code=400, detail="Email already exists")
        return User.from_orm(user)

async def delete_user(user_id: int) -> dict:
    async with SessionLocal() as session:
        user = await session.get(UserModel, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not user.is_active:
            raise HTTPException(status_code=400, detail="User already inactive")
        user.is_active = False
        await session.commit()
        return {"detail": "User deactivated (soft deleted)"} 