# Importacion del modulo de fastapi previamente instalado. El body es para poder recibir los parametos de las petciones POST en l body
from fastapi import  FastAPI
# Importacion de modulo que me permite retornar contenido html
from fastapi.responses import HTMLResponse, JSONResponse
#Importacion de modulo para la creacion de esquemas y dalre mejor manejo a los datos de nuestra api (no hay que instalar)
from pydantic import BaseModel
#Modulo para indicar que el id va ser de tipo entero, (explorar el modulo para ver que mas funcionalidades tiene)
from utils.jwt_manager import create_token
from config.database import engine, Base
from middlewares.error_handler import error_handler
from routers.movie import movie_router
from routers.user import user_router



# Creo una instancia del modulo FastAPI
app = FastAPI()
app.title = "Mi aplicacion con fastAPI"
app.version = "0.0.1"
app.add_middleware(error_handler)
app.include_router(movie_router)
app.include_router(user_router)

Base.metadata.create_all(bind=engine)

@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>HOLA MUNDO</h1>')

