from fastapi import APIRouter

# Importacion del modulo de fastapi previamente instalado. El body es para poder recibir los parametos de las petciones POST en l body
from fastapi import Depends, Path, Query
# Importacion de modulo que me permite retornar contenido html
from fastapi.responses import  JSONResponse

from pydantic import BaseModel, Field
#Modulo para indicar que el id va ser de tipo entero, (explorar el modulo para ver que mas funcionalidades tiene)
from typing import Optional, List
from config.database import session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_beare import JWTBearer
from services.movie import MovieService
from shemas.movie import Movie
movie_router = APIRouter()

@movie_router.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = session()
    result = MovieService(db).get_movies()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

#Ejemplo de parametros de ruta representado por {id}, el cual luego se inyecta como un parametro mas a la funcion get_movie(id)
@movie_router.get('/movies/{id}', tags=['movies'], response_model=Movie, status_code=200)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie :
    db = session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

#Ejemplo de parametros query, los cuales solo se definen en la funcion y en la ruta debe terminar con / para indicar que vienen parametros query, se pueden agregar cuantos quiera
@movie_router.get('/movies/', tags=['movies'], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:

    db = session()
    result = MovieService(db).get_movie_category(category)
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db = session()
    MovieService(db).create_movie(movie)
    return JSONResponse(status_code=201, content={
        "message": "Se a creado la pelicula de forma exitosa"
    }) 

@movie_router.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    db = session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    MovieService(db).update_movie(id,movie)
    return JSONResponse(status_code=200, content={"message": "Se a modificado la pelicula de forma exitosa"})
    
@movie_router.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def delete_movie(id) -> dict:
    db = session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    MovieService(db).delete_movie(id)
    return JSONResponse(status_code=200, content={'message': "Pelicula Eliminada"})