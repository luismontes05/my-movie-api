
#Importacion de modulo para la creacion de esquemas y dalre mejor manejo a los datos de nuestra api (no hay que instalar)
from pydantic import BaseModel

class User(BaseModel):
    email: str
    password: str