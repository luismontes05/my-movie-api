# Importacion del modulo de fastapi previamente instalado. El body es para poder recibir los parametos de las petciones POST en l body
from fastapi import Depends, FastAPI, Body, HTTPException, Path, Query, Request
# Importacion de modulo que me permite retornar contenido html
from fastapi.responses import HTMLResponse, JSONResponse
#Importacion de modulo para la creacion de esquemas y dalre mejor manejo a los datos de nuestra api (no hay que instalar)
from pydantic import BaseModel, Field
#Modulo para indicar que el id va ser de tipo entero, (explorar el modulo para ver que mas funcionalidades tiene)
from typing import Optional, List
#Modulo validador de token
from jwt_manager import create_token, validate_token
#
from fastapi.security import HTTPBearer


# Creo una instancia del modulo FastAPI
app = FastAPI()
app.title = "Mi aplicacion con fastAPI"
app.version = "0.0.1"

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "davidmos.2906@gmail.com":
            raise HTTPException(status_code=403, detail="Credenciales invalidas")

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(default="Mi pelicula", min_length=5, max_length=15)
    overview: str = Field(default="Mi descripcion de la pelicula", min_length=15, max_length=50)
    year: int = Field(default=2022, le=2023)
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_length=5, max_length=15)

    class Config:
        schema_extra = {
            "example":{
                'id': 1,
                'title': 'Avatar',
                'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
                'year': '2022',
                'rating': 9.8,
                'category': 'Ficcion'  
            }
        }

class User(BaseModel):
    email: str
    password: str


movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    },
    {
        'id': 2,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    } 
]

@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>HOLA MUNDO</h1>')

@app.post('/login', tags=['auth'])
def login(user: User):
    if user.email == "davidmos.2906@gmail.com" and user.password == "admin":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)
    else:
        return JSONResponse(status_code=401, content='')

@app.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    return JSONResponse(status_code=200, content=movies)

#Ejemplo de parametros de ruta representado por {id}, el cual luego se inyecta como un parametro mas a la funcion get_movie(id)
@app.get('/movies/{id}', tags=['movie'], response_model=Movie, status_code=200)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie :
    for item in movies:
        if item['id'] == id:
            return JSONResponse(status_code=200, content=item)
    return JSONResponse(status_code=404, content=[])

#Ejemplo de parametros query, los cuales solo se definen en la funcion y en la ruta debe terminar con / para indicar que vienen parametros query, se pueden agregar cuantos quiera
@app.get('/movies/', tags=['movies'], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    data = [movie for movie in movies if movie['category'] == category]
    return JSONResponse(content=data)


@app.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    movies.append(movie)
    return JSONResponse(status_code=201, content={
        "message": "Se a creado la pelicula de forma exitosa"
    }) 

@app.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    for item in movies:
        if item['id'] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
            return JSONResponse(status_code=200, content={
                "message": "Se a modificado la pelicula de forma exitosa"
            }) 

@app.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def delete_movie(id) -> dict:
    for item in movies:
        if item['id'] == id:
            movies.remove(item)
            return JSONResponse(status_code=200, content={
                "message": "Se elimino la pelicula de forma exitosa"
            }) 

