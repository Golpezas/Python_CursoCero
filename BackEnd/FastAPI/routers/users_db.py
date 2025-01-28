from fastapi import APIRouter, HTTPException
from typing import List, Optional
from db.models.user import User
from db.client import db_client

router = APIRouter(prefix="/userdb", tags=["userdb"])

# Inicia el servidor: uvicorn users:app --reload

# Entidad User

users_list = []

@router.get("/")
async def users():
    return users_list

# Path parameters
@router.get("/{id}")
async def get_user_by_id(id: int):
    user = search_user(id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

# Query parameters
@router.get("/")
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

@router.post("/")
async def create_user(new_user: User):
    '''if search_user(new_user.id):
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    users_list.append(new_user)
    return {"message": "Usuario agregado correctamente"}'''

    user_dict = dict(new_user)
    del user_dict["id"]

    db_client.local.users.insert_one(new_user)

@router.put("/")
async def update_user(user: User):
    for i in range(len(users_list)):
        if users_list[i].id == user.id:
            users_list[i] = user
            return {"message": "Usuario actualizado correctamente"}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@router.delete("/{id}")
async def delete_user(id: int):
    for i in range(len(users_list)):
        if users_list[i].id == id:
            del users_list[i]
            return {"message": "Usuario eliminado correctamente"}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")