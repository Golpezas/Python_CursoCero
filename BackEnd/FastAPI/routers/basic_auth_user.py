from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserInDB(User):
    password: str

users_db = {
    "Mamut": {
        "username" : "Mamut",
        "full_name" : "Antonio Hernandez",
        "email" : "mamut@gmm.com",
        "disabled" : False,
        "password" : "1234"
    },
    "mgPrueba": {
        "username" : "mgPrueba",
        "full_name" : "Maria Gonzalez",
        "email" : "mgprueba@gmm.com",
        "disabled" : True,
        "password" : "5432"
    },
    "ppPrueba": {
        "username" : "ppPrueba",
        "full_name" : "Pedro Perez",
        "email" : "ppprueba@gmm.com",
        "disabled" : False,
        "password" : "5678"
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserInDB(**users_db[username])
    return None

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    return None

def current_user(token: str = Depends(oauth2_scheme)):
    user = search_user(token)
    if not user:
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")
    if user.disabled:
        raise HTTPException(status_code=400, detail="Usuario deshabilitado")
    return user
    
@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail="Usuario incorrecto")
    
    user = search_user_db(form.username)

    if not form.password == user.password:
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")
    
    return {"access_token": user.username, "token_type": "bearer"}

@app.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user