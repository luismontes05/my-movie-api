from fastapi import APIRouter
from fastapi.responses import  JSONResponse
#Modulo para indicar que el id va ser de tipo entero, (explorar el modulo para ver que mas funcionalidades tiene)
from utils.jwt_manager import create_token
from shemas.user import User

user_router = APIRouter()

@user_router.post('/login', tags=['auth'])
def login(user: User):
    if user.email == "davidmos.2906@gmail.com" and user.password == "admin":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)
    else:
        return JSONResponse(status_code=401, content='user or password incorrect')   