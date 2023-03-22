from typing import List
from datetime import datetime, timedelta
from sqlalchemy import and_

from sqlalchemy.orm import Session

from src.database.models import User, AuthUser
from src.schemas import UserModel


async def get_users(skip: int, limit: int, db: Session, user: AuthUser) -> List[User]:
    """
    The get_users function returns a list of users from the database.

    :param skip: int: Skip a number of users in the database
    :param limit: int: Limit the number of users returned
    :param db: Session: Access the database
    :param user: AuthUser: Get the user id from the token
    :return: A list of user objects
    :doc-author: Trelent
    """
    return db.query(User).filter(User.authuser_id == user.id).offset(skip).limit(limit).all()


async def get_user(user_id: int, db: Session, user: AuthUser) -> User:
    """
    The get_user function is used to retrieve a user from the database.
    It takes in an integer representing the id of the user, a Session object for connecting to
    the database, and an AuthUser object representing who is making this request. It returns a User object.

    :param user_id: int: Specify the id of the user to get
    :param db: Session: Access the database
    :param user: AuthUser: Ensure that the user is authorized to get the requested user
    :return: A user object
    :doc-author: Trelent
    """
    return db.query(User).filter(and_(User.id == user_id, User.authuser_id == user.id)).first()


async def create_user(body: UserModel, db: Session, user: AuthUser) -> User:
    """
    The create_user function creates a new user in the database.
        Args:
            body (UserModel): The UserModel object to be created.
            db (Session): A Session instance for interacting with the database.

    :param body: UserModel: Get the data from the request body
    :param db: Session: Access the database
    :param user: AuthUser: Get the user id from the authuser object
    :return: A user object
    :doc-author: Trelent
    """
    user = User(first_name=body.first_name,
    second_name=body.second_name, 
    email=body.email, 
    phone=body.phone, 
    birthaday=body.birthaday, 
    description=body.description,
    authuser_id=user.id)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


async def update_user(user_id: int, body: UserModel, db: Session, user: AuthUser) -> User| None:
    """
    The update_user function updates a user in the database.
        Args:
            user_id (int): The id of the user to update.
            body (UserModel): The updated User object with new values for each field.

    :param user_id: int: Identify the user that is being updated
    :param body: UserModel: Pass the json data from the request to update_user function
    :param db: Session: Get the database session
    :param user: AuthUser: Check if the user is logged in and has permission to update the user
    :return: The updated user
    :doc-author: Trelent
    """
    usr= db.query(User).filter(and_(User.id == user_id, User.authuser_id == user.id)).first()
    if usr:
        usr.first_name = body.first_name
        usr.second_name = body.second_name
        usr.email = body.email
        usr.phone = body.phone
        usr.birthaday = body.birthaday
        usr.description = body.description
        usr.authuser_id = user.id
        db.commit()
    return usr


async def remove_user(user_id: int, db: Session, user: AuthUser)  -> User | None:
    """
    The remove_user function removes a user from the database.
        Args:
            user_id (int): The id of the user to be removed.
            db (Session): A connection to the database.
            authuser (AuthUser): The authenticated User object that is making this request.

    :param user_id: int: Identify the user to be deleted
    :param db: Session: Access the database
    :param user: AuthUser: Make sure that the user who is trying to delete a user has permission to do so
    :return: The user that was deleted, or none if no such user exists
    :doc-author: Trelent
    """
    user = db.query(User).filter(and_(User.id == user_id, User.authuser_id == user.id)).first()
    if user:
        db.delete(user)
        db.commit()
    return user


async def get_users_by_some_info(some_info: str, db: Session, user: AuthUser) -> List[User]:
    """
    The get_users_by_some_info function takes a string and returns all users that have the string in their first name, second name or email.
        Args:
            some_info (str): The search term to be used for finding users.
            db (Session): A database session object.
            user (AuthUser): An AuthUser object representing the current user of the application.

    :param some_info: str: Search for a user by first name, second name or email
    :param db: Session: Access the database
    :param user: AuthUser: Get the id of the user who is logged in
    :return: A list of users whose first name, second name or email matches the search query
    :doc-author: Trelent
    """
    response = []
    info_by_first_name = db.query(User).filter(and_(User.first_name.like(f'%{some_info}%'), User.authuser_id == user.id)).all()
    if info_by_first_name:
        for n in info_by_first_name:
            response.append(n)
    info_by_second_name = db.query(User).filter(and_(User.second_name.like(f'%{some_info}%'), User.authuser_id == user.id)).all()
    if info_by_second_name:
        for n in info_by_second_name:
            response.append(n)
    info_by_email = db.query(User).filter(and_(User.email.like(f'%{some_info}%'), User.authuser_id == user.id)).all()
    if info_by_email:
        for n in info_by_email:
            response.append(n)
            
    return response


async def get_birthday_per_week(days: int, db: Session, user: AuthUser) -> User:
    """
    The get_birthday_per_week function returns a list of users whose birthday is within the next week.
        Args:
            days (int): The number of days to look ahead for birthdays.
            db (Session): A database session object that can be used to query the database.
            user (AuthUser): An AuthUser object representing the currently logged in user, who will be used as a filter on our query.

    :param days: int: Define the amount of days in which we want to search for birthdays
    :param db: Session: Pass the database session to the function
    :param user: AuthUser: Get the user id from the authuser table
    :return: A list of users whose birthday is in the next 7 days
    :doc-author: Trelent
    """
    response = []
    all_users = db.query(User).filter(User.authuser_id == user.id).all()
    for usr in all_users:
        if timedelta(0) <= ((usr.birthaday.replace(year=int((datetime.now()).year))) - datetime.now().date()) <= timedelta(days):
            response.append(usr)

    return response

