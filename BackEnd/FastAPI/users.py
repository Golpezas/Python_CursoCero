from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Inicia el server: uvicorn users:app --reload

# Entidad user

class user(BaseModel):
    id: int
    Nombre: str
    Apellido: str
    Edad: int
    url: str

def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"message": "Usuario no encontrado"}

users_list = [user(id = 1, Nombre = "Antonio", Apellido = "Hernandez", Edad = 42, url = "https://mouredev.com/python"),
              user(id = 2, Nombre = "Maria", Apellido = "Gonzalez", Edad = 35, url = "https://mouredev123.com/python"),
              user(id = 3, Nombre = "Pedro", Apellido = "Perez", Edad = 25, url = "https://mouredev321.com/python")]         

@app.get("/usersjson")
async def usersjson():
    return [{"Nombre": "Antonio", "Apellido": "Hernandez", "Edad": 42, "url": "https://mouredev.com/python"},
            {"Nombre": "Maria", "Apellido": "Gonzalez", "Edad": 35, "url": "https://mouredev123.com/python"},
            {"Nombre": "Pedro", "Apellido": "Perez", "Edad": 25, "url": "https://mouredev321.com/python"}]

@app.get("/users")
async def users():
    return users_list

#path parameters
@app.get("/user/{id}")
async def user(id: int):
    return search_user(id)

#query parameters
@app.get("/user/")
async def user(id: int):
    return search_user(id)

