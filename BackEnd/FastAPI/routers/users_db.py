# routers/users_db.py
from fastapi import APIRouter, HTTPException
from typing import List
from db.models.user import User
from db.client import db
from db.schemas.user import user_schema, users_schema
from bson import ObjectId

router = APIRouter(prefix="/userdb", tags=["userdb"])

@router.get("/", response_model=List[User])
async def users():
    """
    Devuelve una lista de todos los usuarios en la base de datos.
    """
    return users_schema(db["users"].find())

@router.get("/{id}")
async def get_user_by_id(id: str):
    """
    Devuelve un usuario por su ID.
    """
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="id no valido")
    user = search_user("_id", ObjectId(id))
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@router.get("/search/")
async def get_user_by_query(id: str):
    """
    Devuelve un usuario basado en una consulta por ID.
    """
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="id no valido")
    user = search_user("_id", ObjectId(id))
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@router.post("/", response_model=User)
async def create_user(user: User):
    """
    Crea un nuevo usuario en la base de datos.
    """
    # Verifica si el email ya está en uso
    if search_user("email", user.email) is not None:
        raise HTTPException(status_code=400, detail="El email ya está en uso")
    
    # Convierte el usuario a un diccionario y elimina el campo id si existe
    user_dict = user.dict()
    user_dict.pop("id", None)

    # Inserta el nuevo usuario en la base de datos
    id = db["users"].insert_one(user_dict).inserted_id

    # Recupera el usuario recién creado
    new_user = user_schema(db["users"].find_one({"_id": id}))

    return User(**new_user)

@router.put("/update/{id}")
async def update_user(id: str, user: User):
    """
    Actualiza un usuario existente en la base de datos.
    """
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="id no valido")
    if search_user("_id", ObjectId(id)) is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    user_dict = dict(user)
    del user_dict["id"]

    db["users"].update_one({"_id": ObjectId(id)}, {"$set": user_dict})

    updated_user = user_schema(db["users"].find_one({"_id": ObjectId(id)}))

    return User(**updated_user)

@router.delete("/{id}")
async def delete_user(id: str):
    """
    Elimina un usuario de la base de datos por su ID.
    """
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="id no valido")
    user = search_user("_id", ObjectId(id))
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db["users"].delete_one({"_id": ObjectId(id)})
    return {"message": "Usuario eliminado correctamente"}

def search_user(field: str, key):
    """
    Busca un usuario en la base de datos por un campo y una clave específicos.
    """
    try:
        user = db["users"].find_one({field: key})
        return user_schema(user)
    except:
        return None

# Documentación de cambios:
# 1. Se añadió validación para ObjectId en las rutas que utilizan identificadores.
# 2. Se cambió la ruta de la función `update_user` a `/update/{id}` para evitar conflictos de rutas.
# 3. Se añadió una ruta de búsqueda basada en query parameters.
# 4. Se documentaron todas las funciones con comentarios para una mejor revisión.