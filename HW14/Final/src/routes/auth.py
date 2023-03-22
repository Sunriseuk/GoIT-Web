from fastapi import APIRouter, HTTPException, Depends, status, Security, BackgroundTasks, Request
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import AuthUserModel, AuthUserResponse, TokenModel, RequestEmail
from src.repository import authusers as repository_users
from src.services.auth import auth_service

from src.services.email import send_email

router = APIRouter(prefix='/auth', tags=["auth"])
security = HTTPBearer()


@router.post("/signup", response_model=AuthUserResponse, status_code=status.HTTP_201_CREATED)
async def signup(body: AuthUserModel, background_tasks: BackgroundTasks, request: Request, db: Session = Depends(get_db)):
    """
    The signup function creates a new user in the database.
        It takes an AuthUserModel object as input, which contains the username and email of the new user.
        The password is hashed using Argon2 before being stored in the database.
        A background task is created to send a confirmation email to the newly registered user.

    :param body: AuthUserModel: Get the data from the request body
    :param background_tasks: BackgroundTasks: Add a task to the background queue
    :param request: Request: Get the base url of the application
    :param db: Session: Pass the database session to the function
    :return: A dictionary, which is not a valid response
    :doc-author: Trelent
    """
    exist_user = await repository_users.get_authuser_by_email(body.email, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists")
    body.password = auth_service.get_password_hash(body.password)
    new_user = await repository_users.create_authuser(body, db)
    background_tasks.add_task(send_email, new_user.email, new_user.username, request.base_url)
    return {"user": new_user, "detail": "User successfully created. Check your email for confirmation."}


@router.post("/login", response_model=TokenModel)
async def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
        The login function is used to authenticate a user.
            It takes in the username and password of the user, and returns an access token if successful.
            The access token can be used to make authenticated requests for data from the API.

        :param body: OAuth2PasswordRequestForm: Get the username and password from the request body
        :param db: Session: Get a database session from the dependency injection container
        :return: A dictionary with the access token, refresh token and a bearer type
        :doc-author: Trelent
        """
    user = await repository_users.get_authuser_by_email(body.username, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email")
    if not user.confirmed:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not confirmed")
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    # Generate JWT
    access_token = await auth_service.create_access_token(data={"sub": user.email}, expires_delta=7200)
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})
    await repository_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get('/refresh_token', response_model=TokenModel)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    """
    The refresh_token function is used to refresh the access token.
        The function takes in a refresh token and returns an access_token, a new refresh_token, and the type of token.
        If the user's current refresh_token does not match what was passed into this function then it will return an error.

    :param credentials: HTTPAuthorizationCredentials: Get the token from the request header
    :param db: Session: Access the database
    :return: A dictionary with the access_token, refresh_token and token type
    :doc-author: Trelent
    """
    token = credentials.credentials
    email = await auth_service.decode_refresh_token(token)
    user = await repository_users.get_authuser_by_email(email, db)
    if user.refresh_token != token:
        await repository_users.update_token(user, None, db)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    access_token = await auth_service.create_access_token(data={"sub": email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": email})
    await repository_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get('/confirmed_email/{token}')
async def confirmed_email(token: str, db: Session = Depends(get_db)):
    """
    The confirmed_email function is used to confirm a user's email address.
        It takes the token from the URL and uses it to get the user's email address.
        The function then checks if there is a user with that email in our database, and if not, returns an error message.
        If there is a matching record in our database, we check whether or not their account has already been confirmed;
            if so, we return another message saying as much; otherwise we update their record by setting confirmed=True.

    :param token: str: Get the token from the url
    :param db: Session: Get the database session
    :return: A message to the user that their email is already confirmed
    :doc-author: Trelent
    """
    email = await auth_service.get_email_from_token(token)
    user = await repository_users.get_authuser_by_email(email, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error")
    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    await repository_users.confirmed_email(email, db)
    return {"message": "Email confirmed"}


@router.post('/request_email')
async def request_email(body: RequestEmail, background_tasks: BackgroundTasks, request: Request,
                        db: Session = Depends(get_db)):
    """
    The request_email function is used to send an email to the user with a link that will allow them
    to confirm their account. The function takes in a RequestEmail object, which contains the email of
    the user who wants to confirm their account. It then checks if there is already an unconfirmed
    account associated with that email address, and if so it sends an email containing a confirmation link.

    :param body: RequestEmail: Get the email from the request body
    :param background_tasks: BackgroundTasks: Add a task to the background tasks queue
    :param request: Request: Get the base_url of the application
    :param db: Session: Get the database session
    :return: A dict with a message key
    :doc-author: Trelent
    """
    user = await repository_users.get_authuser_by_email(body.email, db)

    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    if user:
        background_tasks.add_task(send_email, user.email, user.username, request.base_url)
    return {"message": "Check your email for confirmation."}