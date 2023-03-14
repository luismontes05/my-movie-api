#Importacion de modulo para la creacion de esquemas y dalre mejor manejo a los datos de nuestra api (no hay que instalar)
from pydantic import BaseModel, Field
from typing import Optional, List


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