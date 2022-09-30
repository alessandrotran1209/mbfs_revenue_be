from fastapi import FastAPI, Depends, HTTPException
from starlette.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from controllers.Auth import Auth

from models.RevenueTarget import RevenueTarget
from controllers import Controller as controller
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from typing import List

from models.RevenueUpdate import RevenueUpdate
from models.TokenSchema import TokenSchema
from models.UserAuth import UserAuth
from utils.utils import create_access_token, create_refresh_token, verify_password, get_hashed_password

app = FastAPI()
origins = [
    # "http://localhost:4200",
    # "https://mobi-hatang.herokuapp.com",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post('/login', summary="Create access and refresh tokens for user")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    account = Auth()
    user = account.get_user(form_data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    hashed_pass = user['password']
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    return {
        "access_token": create_access_token(user['username']),
        "refresh_token": create_refresh_token(user['username']),
        "username": user['username']
    }


@app.post('/signup', summary="Create new user")
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


@app.post("/insert")
async def insert_revenue(revenue_target: RevenueTarget):
    completed = controller.insert(revenue_target.__dict__)
    if completed:
        return JSONResponse(status_code=200, content={"data": completed})
    return JSONResponse(status_code=500, content={"data": completed})


@app.post("/update-week")
async def update_week_revenue(revenue_update: RevenueUpdate):
    completed = controller.update(revenue_update.__dict__)
    print(revenue_update.__dict__)
    if completed:
        return JSONResponse(status_code=200, content={"data": completed})
    return JSONResponse(status_code=500, content={"data": completed})


@app.get("/revenue/q")
async def get_revenue_from_sources(source: str):
    categories = controller.get_revenue_from_source(source)
    return JSONResponse(status_code=200, content={"data": categories})


@app.get("/category/q")
async def get_category_suggestion(source: str):
    categories = controller.get_category_suggestion(source)
    return JSONResponse(status_code=200, content={"data": categories})


@app.get("/subcategory/q")
async def get_subcategory_suggestion(source: str, category: str):
    subcategories = controller.get_subcategory_suggestion(source, category)
    return JSONResponse(status_code=200, content={"data": subcategories})


@app.get("/detail/q")
async def get_detail_suggestion(source: str, category: str, subcategory: str):
    details = controller.get_detail_suggestion(source, category, subcategory)
    print(details)
    return JSONResponse(status_code=200, content={"data": details})


@app.post("/insert-excel")
async def insert_revenue_excel(revenue_target: List[RevenueTarget]):
    completed = controller.insert_excel(revenue_target)
    return JSONResponse(status_code=200, content={"data": True})
# @app.post("/other")
# async def insert_internal_revenue():
#     return {"message": "Hello World"}
