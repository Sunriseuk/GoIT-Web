from sqlalchemy.orm import Session

from src.database.models import AuthUser
from src.schemas import AuthUserModel

from libgravatar import Gravatar


async def get_authuser_by_email(email: str, db: Session) -> AuthUser:
    """
    The get_authuser_by_email function takes in an email and a database session,
    and returns the AuthUser object that has the given email. If no such user exists,
    it returns None.

    :param email: str: Pass in the email address of a user
    :param db: Session: Pass the database session to the function
    :return: An authuser object
    :doc-author: Trelent
    """
    return db.query(AuthUser).filter(AuthUser.email == email).first()


async def create_authuser(body: AuthUserModel, db: Session) -> AuthUser:
    """
    The create_authuser function creates a new user in the database.
        Args:
            body (AuthUserModel): The AuthUserModel object to be created.
            db (Session): The SQLAlchemy session object used for querying the database.

    :param body: AuthUserModel: Pass the authusermodel object from the request body
    :param db: Session: Access the database
    :return: The new user object
    :doc-author: Trelent
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = AuthUser(**body.dict(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: AuthUser, token: str | None, db: Session) -> None:
    """
    The update_token function updates the refresh token for a user.

    :param user: AuthUser: Get the user's id
    :param token: str | None: Update the refresh token in the database
    :param db: Session: Update the database with the new refresh token
    :return: None
    :doc-author: Trelent
    """
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    """
    The confirmed_email function takes in an email and a database session,
    and sets the confirmed field of the user with that email to True.


    :param email: str: Get the email of the user
    :param db: Session: Pass the database session to the function
    :return: None
    :doc-author: Trelent
    """
    user = await get_authuser_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email, url: str, db: Session) -> AuthUser:
    """
    The update_avatar function updates the avatar of a user.
        Args:
            email (str): The email of the user to update.
            url (str): The new URL for the avatar image.

    :param email: Get the user from the database
    :param url: str: Specify the type of data that is expected to be passed in
    :param db: Session: Pass the database session to the function
    :return: The updated user
    :doc-author: Trelent
    """
    user = await get_authuser_by_email(email, db)
    user.avatar = url
    db.commit()
    return user
