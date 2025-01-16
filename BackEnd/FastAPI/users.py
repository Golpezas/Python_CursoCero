from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Inicia el servidor: uvicorn users:app --reload

# Entidad User

class User(BaseModel):
    id: int
    Nombre: str
    Apellido: str
    Edad: int
    url: str

users_list = [
    User(id=1, Nombre="Antonio", Apellido="Hernandez", Edad=42, url="https://mouredev.com/python"),
    User(id=2, Nombre="Maria", Apellido="Gonzalez", Edad=35, url="https://mouredev123.com/python"),
    User(id=3, Nombre="Pedro", Apellido="Perez", Edad=25, url="https://mouredev321.com/python")
]

@app.get("/usersjson")
async def usersjson():
    return [
        {"Nombre": "Antonio", "Apellido": "Hernandez", "Edad": 42, "url": "https://mouredev.com/python"},
        {"Nombre": "Maria", "Apellido": "Gonzalez", "Edad": 35, "url": "https://mouredev123.com/python"},
        {"Nombre": "Pedro", "Apellido": "Perez", "Edad": 25, "url": "https://mouredev321.com/python"}
    ]

@app.get("/users")
async def users():
    return users_list

# Path parameters
@app.get("/user/{id}")
async def get_user_by_id(id: int):
    user = search_user(id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

# Query parameters
@app.get("/user/")
async def get_user_by_query(id: int):
    user = search_user(id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

def search_user(id: int) -> Optional[User]:
    for user in users_list:
        if user.id == id:
            return user
    return None

@app.post("/user")
async def create_user(new_user: User):
    if search_user(new_user.id):
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    users_list.append(new_user)
    return {"message": "Usuario agregado correctamente"}