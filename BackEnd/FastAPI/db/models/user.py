from pydantic import BaseModel

class User(BaseModel):
    id: str | None
    Nombre: str
    Apellido: str
    Edad: int
    url: str