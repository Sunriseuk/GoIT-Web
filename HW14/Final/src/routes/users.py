from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session


from src.database.db import get_db
from src.database.models import AuthUser
from src.schemas import UserModel, UserResponse
from src.repository import users as repository_users
from src.services.auth import auth_service

router = APIRouter(prefix='/users', tags=["users"])


@router.get("/all", response_model=List[UserResponse], description='No more than 1 requests per 3 minute',
            dependencies=[Depends(RateLimiter(times=15, seconds=120))])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                     current_user: AuthUser = Depends(auth_service.get_current_user)):
    """
    The read_users function returns a list of users.

    :param skip: int: Skip a number of users
    :param limit: int: Specify the maximum number of users to return
    :param db: Session: Pass the database session to the repository
    :param current_user: AuthUser: Get the current user from the database
    :return: A list of users
    :doc-author: Trelent
    """
    users = await repository_users.get_users(skip, limit, db, current_user)
    return users

