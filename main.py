# Importacion del modulo de fastapi previamente instalado. El body es para poder recibir los parametos de las petciones POST en l body
from fastapi import FastAPI, Body
# Importacion de modulo que me permite retornar contenido html
from fastapi.responses import HTMLResponse


# Creo una instancia del modulo FastAPI
app = FastAPI()
app.title = "Mi aplicacion con fastAPI"
app.version = "0.0.1"

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

@app.get('/movies', tags=['movies'])
def get_movies():
    return movies

#Ejemplo de parametros de ruta representado por {id}, el cual luego se inyecta como un parametro mas a la funcion get_movie(id)
@app.get('/movies/{id}', tags=['movie'])
def get_movie(id: int):
    for item in movies:
        if item['id'] == id:
            return item
    return[]

#Ejemplo de parametros query, los cuales solo se definen en la funcion y en la ruta debe terminar con / para indicar que vienen parametros query, se pueden agregar cuantos quiera
@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str):
    return [movie for movie in movies if movie['category'] == category]


@app.post('/movies', tags=['movies'])
def create_movie(id: int = Body(), title: str = Body(), overview: str = Body(), year: int = Body(), rating: float = Body(), category: str = Body()):
    movies.append({
        "id": id,
        "title": title,
        "overview": overview,
        "year": year,
        "rating": rating,
        "category": category  
    })
    return movies