# Importacion del modulo de fastapi previamente instalado. El body es para poder recibir los parametos de las petciones POST en l body
from fastapi import FastAPI, Body, Path, Query
# Importacion de modulo que me permite retornar contenido html
from fastapi.responses import HTMLResponse, JSONResponse
#Importacion de modulo para la creacion de esquemas y dalre mejor manejo a los datos de nuestra api (no hay que instalar)
from pydantic import BaseModel, Field
#Modulo para indicar que el id va ser de tipo entero, (explorar el modulo para ver que mas funcionalidades tiene)
from typing import Optional, List


# Creo una instancia del modulo FastAPI
app = FastAPI()
app.title = "Mi aplicacion con fastAPI"
app.version = "0.0.1"

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

@app.get('/movies', tags=['movies'], response_model=List[Movie])
def get_movies() -> List[Movie]:
    return JSONResponse(content=movies)

#Ejemplo de parametros de ruta representado por {id}, el cual luego se inyecta como un parametro mas a la funcion get_movie(id)
@app.get('/movies/{id}', tags=['movie'], response_model=Movie)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie :
    for item in movies:
        if item['id'] == id:
            return JSONResponse(content=item)
    return JSONResponse(content=[])

#Ejemplo de parametros query, los cuales solo se definen en la funcion y en la ruta debe terminar con / para indicar que vienen parametros query, se pueden agregar cuantos quiera
@app.get('/movies/', tags=['movies'], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    data = [movie for movie in movies if movie['category'] == category]
    return JSONResponse(content=data)


@app.post('/movies', tags=['movies'], response_model=dict)
def create_movie(movie: Movie) -> dict:
    movies.append(movie)
    return JSONResponse(content={
        "message": "Se a creado la pelicula de forma exitosa"
    }) 

@app.put('/movies/{id}', tags=['movies'], response_model=dict)
def update_movie(id: int, movie: Movie) -> dict:
    for item in movies:
        if item['id'] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
            return JSONResponse(content={
                "message": "Se a modificado la pelicula de forma exitosa"
            }) 

@app.delete('/movies/{id}', tags=['movies'], response_model=dict)
def delete_movie(id) -> dict:
    for item in movies:
        if item['id'] == id:
            movies.remove(item)
            return JSONResponse(content={
                "message": "Se elimino la pelicula de forma exitosa"
            }) 

