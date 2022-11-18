from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from starlette.responses import JSONResponse
from starlette import status

from controllers.Auth import Auth
from models.UserAuth import UserAuth

from utils.utils import create_access_token, create_refresh_token, verify_password, get_hashed_password

router = APIRouter()


@router.post('/login', summary="Create access and refresh tokens for user")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    account = Auth()
    user = account.get_user(form_data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )
    hashed_pass = user['password']
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )
    return {
        "access_token": create_access_token(user['username']),
        "refresh_token": create_refresh_token(user['username']),
        "username": user['username']
    }


@router.post('/signup', summary="Create new user")
async def create_user(data: UserAuth):
    user = {
        'username': data.username,
        'password': get_hashed_password(data.password),
    }

    auth = Auth()
    result = auth.insert_user(user)
    if result:
        return {
            'username': data.username,
            'password': get_hashed_password(data.password),
        }
    return JSONResponse(status_code=500, content={"data": "Something went wrong"})
